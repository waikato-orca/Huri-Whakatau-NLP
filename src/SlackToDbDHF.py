# Program stores Slack workspace data from json files into a database
# with pre-created tables provided in schema.sql
#
# Instructions:
#   Start up database
#   Ensure database name matches the one in this program - default: jr_slack
#   Create db tables using the schema.sql file
#   Run program:
#       For each Slack workspace/folder:
#           1) File -> Open Users -> browse to open users.json
#           2) File -> Open Channels -> browse to open channels.json
#           3) File -> Open Posts -> browse to open folder containing discussion json files (dates as file names)
#
# Last query: if query breaks, run last query to see what broke

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# import requests
import json
import copy
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import textwrap
from typing import List, Dict, Set
import sqlreader as fr

class Slack2Db:
    root = None
    mainframe = None
    main_text = None
    count = 0
    reader = None
    max_dprint = 60
    slack_token = 'xoxp-526437257302-526074640887-579146000418-b6780f79b3d0f23dd1796ec14c15859e'

    # Constructor
    def __init__(self, root, version: str):
        self.root = root
        self.root.title("Slack/DB IO {}".format(version))
        self.mainframe = ttk.Frame(self.root, borderwidth=2, relief="groove")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.create_menus()
        self.create_widgets()
        self.set_resize()

        # Connect to database - args[username, password, dbname, enable writes]
        self.reader = fr.sqlReader(
            "root", "123456789", "jr_slack", True)

    def create_menus(self):
        print("adding menus")
        self.root.option_add('*tearOff', FALSE)
        menubar = Menu(self.root)
        self.root['menu'] = menubar
        menu_file = Menu(menubar)
        menu_database = Menu(menubar)

        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_database, label='Database')

        menu_file.add_command(label='Open Users', command=self.open_users)
        menu_file.add_command(label='Open Channels',
                              command=self.open_channels)
        menu_file.add_command(label='Open Posts', command=self.open_posts)
        menu_file.add_command(label='Exit', command=self.terminate)

        menu_database.add_command(label='Clear all', command=self.clear_all)
        menu_database.add_command(label='Last Query', command=self.last_query)

    def create_widgets(self):
        print("adding widgets")
        self.main_text = Text(self.mainframe, width=80, height=20)
        self.main_text.grid(column=0, row=0, sticky=(N, W, E, S))

        text_scrollbar = ttk.Scrollbar(
            self.mainframe, orient=VERTICAL, command=self.main_text.yview)
        self.main_text['yscrollcommand'] = text_scrollbar.set
        text_scrollbar.grid(column=1, row=0, sticky=(N, S))

    def set_resize(self):
        print("adding resizing")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

    # Creates an sql REPLACE query to insert an element from a json file to the db
    # dict: the element from the json file to insert
    # table_name: the table to insert the element
    # skip_list: a list of json fields to exclude from the query
    # -> str: returns the sql query
    def create_dict_insert(self, dict: Dict, table_name: str, skip_list: List = [], command_type: str = "REPLACE") -> str:
        sql_str_bgn = "{} INTO {} (".format(command_type, table_name)
        sql_str_end = ") VALUES ("
        for key, val in dict.items():
            if key not in skip_list:
                # Append column keys into column part of sql: (key1, key2, ...
                sql_str_bgn += "`{}`, ".format(key)
                # Append values into VALUES part of sql: ) VALUES (val1, val2, ...
                sql_str_end += "{}, ".format(self.reader.escape_text(val))

        # Combine keys and values of sql statement
        sql = "{}{});".format(sql_str_bgn, sql_str_end)
        sql = sql.replace(", )", ")")
        return sql

    # Creates a list of REPLACE queries to insert an array/list element from a json file to the db
    # list: the list element from the json file to insert
    # table_name: the table to insert the element
    # parent_id: the id/key of the db entry that the list elements are connected to
    # skip_list: a list of json fields to exclude from the query
    def create_list_insert(self, list: List, table_name: str, parent_id: str, column_name: str, skip_list: List = [], command_type: str = "REPLACE"):
        sql_list = []

        # Handle dictionary elements
        if isinstance(list[0], dict):
            for i in range(len(list)):

                # Append `parent_id` and `id` fields to dictionary element
                list[i]["parent_id"] = parent_id
                list[i]["id"] = parent_id + str(i)

                # Create and append new sql statement to sql insert list
                sql = self.create_dict_insert(
                    list[i], table_name, skip_list)
                sql_list.append(sql)
        else:
            # Handle single elements
            sql = "{} INTO {} (id, {}, parent_id) VALUES ".format(
                command_type, table_name, column_name)
            for entry in range(len(list)):
                entry_id = parent_id + str(entry)
                sql += "({}, {}, {}), ".format(self.reader.escape_text(entry_id),
                                               self.reader.escape_text(list[entry]), self.reader.escape_text(parent_id))
            sql += ";"
            sql = sql.replace(", ;", ";")
            sql_list.append(sql)
        return sql_list

    def buld_max_post(self, key: str, val, dct: Dict):
        if isinstance(val, (list, dict, set)):
            return
        k = key
        if k not in dct.keys():
            dct[k] = val
        else:
            if type(val) is str and type(dct[k]) is str:
                if len(val) > len(dct[k]):
                    dct[k] = val
            else:
                dct[k] = max(dct[k], val)

    def last_query(self):
        strlen = self.max_dprint
        self.max_dprint = -1
        self.dprint(self.reader.get_last_query())
        self.max_dprint = strlen

    # Deletes all rows from all tables in the database
    def clear_all(self):
        self.dprint("Truncating all tables")
        self.reader.write_data("truncate t_user;")
        self.reader.write_data("truncate t_user_profile;")
        self.reader.write_data("truncate t_channel;")
        self.reader.write_data("truncate t_channel_pins")
        self.reader.write_data("truncate t_channel_members;")
        self.reader.write_data("truncate t_channel_purpose;")
        self.reader.write_data("truncate t_channel_topic;")
        self.reader.write_data("truncate t_message;")
        self.reader.write_data("truncate t_message_files;")
        self.reader.write_data("truncate t_message_reactions;")
        self.reader.write_data("truncate t_message_reactions_users;")
        self.reader.write_data("truncate t_message_root;")
        self.reader.write_data("truncate t_message_root_reply_users;")
        self.reader.write_data("truncate t_message_edited;")
        self.reader.write_data("truncate t_message_replies;")
        self.reader.write_data("truncate t_message_reply_users;")
        self.dprint("Finished truncating all tables")

    # def handle_file_entries(self, entry: Dict, files_dict: Dict, use_local: bool = False) -> str:
    #     to_return = ""
    #     return to_return  # make the rest of the code unreachable
    #     for mf in entry["files"]:
    #         mf["user"] = entry["user"]
    #         mf["ts"] = entry["ts"]
    #         if mf["pretty_type"] == "Post":
    #             if use_local:
    #                 to_return += mf["preview"]
    #             else:
    #                 url = mf["url_private"]
    #                 try:
    #                     result = requests.get(
    #                         url, headers={'Authorization': 'Bearer %s' % self.slack_token})
    #                     dict = json.loads(result.text)
    #                     root = dict["root"]
    #                     to_return = ""
    #                     ch_list = root["children"]
    #                     for ch in ch_list:
    #                         if ch["type"] == 'p':
    #                             to_return += "{} ".format(ch["text"])
    #                     print("handle_file_entries(): text = {}".format(to_return))
    #                 except requests.exceptions.RequestException as err:
    #                     print("Got a RequestException: {}".format(err))
    #                     to_return += mf["preview"]
    #         sql = self.create_dict_insert(mf, "t_message_files", [
    #             "image_72", "has_rich_preview", "thumb_360_gif", "thumb_480_gif", "deanimate_gif"])
    #         self.dprint(sql)
    #         self.reader.write_data(sql)
    #         for key, val in mf.items():
    #             self.buld_max_post(key, val, files_dict)
    #     return to_return

    # Reads all data from folder selected from dialog box and writes all the data to database
    def open_posts(self):
        # List of fields to ignore and not write to the `t_message` table in the db
        ignore_list = ["subscribed", "team", "user_team", "files", "upload", "display_as_bot",
                       "source_team", "user_profile", "edited", "blocks", "reactions", "replies", "reply_users", "root"]
        self.dprint("open Slack post files")
        message_dict = {"dirname": "my_dir",
                        "filename": "my_file", "id_str": "abcdefg"}
        files_dict = {"user": "FFGREB4Q0", "ts": '1547837708.000300'}
        dirname = filedialog.askdirectory()
        if dirname:
            cdir = Path(dirname).name
            self.dprint("open_posts(): opening {}".format(cdir))
            onlyfiles = [f for f in listdir(
                dirname) if isfile(join(dirname, f))]
            os.chdir(dirname)
            for filename in onlyfiles:
                self.dprint("open_posts(): opening {}".format(filename))
                if filename.endswith(".json"):
                    f = open(filename, 'r', encoding="utf8", errors='ignore')
                    lines = f.read()
                    f.close()
                    dict = json.loads(lines)
                    self.dprint(("# ---------------Post\n"))
                    sequential_text = ""
                    cur_user = ""
                    cur_entry = []
                    write_last_entry = False
                    for entry in dict:
                        entry["dirname"] = cdir
                        entry["filename"] = filename
                        username = "bot"

                        # The current message being read in the json file
                        cur_entry = copy.deepcopy(entry)

                        # Create id_str for t_message insert
                        h = hash(entry['text'])
                        cur_entry["id_str"] = "{}-{}".format(entry["ts"], h)

                        # Write data for the current message/post
                        sql = self.create_dict_insert(
                            cur_entry, "t_message", ignore_list)
                        self.dprint(sql)
                        self.reader.write_data(sql)

                        # Handle `files` field of the current message/post
                        if "files" in cur_entry:
                            files_list = cur_entry["files"]
                            sql_list = self.create_list_insert(
                                files_list, "t_message_files", cur_entry["id_str"], "")
                            for sql in sql_list:
                                self.dprint(sql)
                                self.reader.write_data(sql)

                        # Handle `reactions` field of the current message/post
                        if "reactions" in cur_entry:
                            reactions_list = cur_entry["reactions"]
                            sql_list = self.create_list_insert(
                                reactions_list, "t_message_reactions", cur_entry["id_str"], "", ["users"])
                            for sql in sql_list:
                                self.dprint(sql)
                                self.reader.write_data(sql)

                            for reaction in reactions_list:
                                users_list = reaction["users"]
                                sql_list = self.create_list_insert(
                                    users_list, "t_message_reactions_users", reaction["id"], "user")
                                for sql in sql_list:
                                    self.dprint(sql)
                                    self.reader.write_data(sql)

                        # Handle `reply_users` and `replies` fields of the current message/post
                        if "reply_users" in cur_entry:
                            user_list = cur_entry["reply_users"]
                            sql_list = self.create_list_insert(
                                user_list, "t_message_reply_users", cur_entry["id_str"], "user")
                            for sql in sql_list:
                                self.dprint(sql)
                                self.reader.write_data(sql)

                            replies_list = cur_entry["replies"]
                            sql_list = self.create_list_insert(
                                replies_list, "t_message_replies", cur_entry["id_str"], "")
                            for sql in sql_list:
                                self.dprint(sql)
                                self.reader.write_data(sql)

                        # Handle `edited` field of the current message/post
                        if "edited" in cur_entry:
                            edited_dict = cur_entry["edited"]
                            edited_dict["parent_id"] = cur_entry["id_str"]
                            sql = self.create_dict_insert(
                                edited_dict, "t_message_edited")
                            self.dprint(sql)
                            self.reader.write_data(sql)

                        # Handle `root` field of the current message/post
                        if "root" in cur_entry:
                            root_dict = cur_entry["root"]
                            root_dict["parent_id"] = cur_entry["id_str"]
                            sql = self.create_dict_insert(
                                root_dict, "t_message_root", ["blocks", "reply_users"])
                            self.dprint(sql)
                            self.reader.write_data(sql)

                            reply_users_list = root_dict["reply_users"]
                            sql_list = self.create_list_insert(
                                reply_users_list, "t_message_root_reply_users", root_dict["parent_id"], "user")
                            for sql in sql_list:
                                self.dprint(sql)
                                self.reader.write_data(sql)

                        for key, val in entry.items():
                            self.buld_max_post(key, val, message_dict)

                    # write out the last entry
                    sql = self.create_dict_insert(
                        cur_entry, "t_message", ignore_list)
                    self.dprint(sql)
                    self.reader.write_data(sql)

        self.dprint("Finished open_posts")

    # Reads the selected users.json file and writes the data to the `t_user` table in the database
    def open_users(self):
        self.dprint("open Slack user file")
        filename = filedialog.askopenfilename()
        if filename:
            self.dprint("open_users(): opening {}".format(filename))
            f = open(filename, 'r', encoding="utf8", errors='ignore')
            lines = f.read()
            f.close()
            dict_list = json.loads(lines)

            # Insert each user into the db
            for entry in dict_list:
                self.dprint(
                    ("---------------begin User [{}]\n".format(entry["name"])))
                # Write user data into db
                sql = self.create_dict_insert(entry, "t_user", ["profile"])
                self.dprint(sql)
                self.reader.write_data(sql)

                # Write profile field of user data to the db
                profile_dict = entry["profile"]
                profile_dict["parent_id"] = entry["id"]
                sql = self.create_dict_insert(profile_dict, "t_user_profile", [
                    "fields", "guest_channels"])
                self.dprint(sql)
                self.reader.write_data(sql)

        self.dprint("Finished open_users")

    # Reads the selected channels.json file and writes the data to the `t_channels` table in the database
    def open_channels(self):
        self.dprint("open Slack channel file")
        filename = filedialog.askopenfilename()
        if filename:
            self.dprint("open_channels(): opening {}".format(filename))
            f = open(filename, 'r', encoding="utf8", errors='ignore')
            lines = f.read()
            f.close()
            dict_list = json.loads(lines)

            # Write each channel into the db
            for entry in dict_list:
                self.dprint(
                    ("# --------------- Channel {}\n".format(entry["name"])))

                # Write general channel data into the db
                sql = self.create_dict_insert(
                    entry, "t_channel", ["topic", "purpose", "members", "pins"])
                self.dprint(sql)
                self.reader.write_data(sql)

                # Handle `members` field of the current channel
                member_list = entry["members"]
                if len(member_list) > 0:
                    sql_list = self.create_list_insert(
                        member_list, "t_channel_members", entry["id"], "member")
                    for sql in sql_list:
                        self.dprint(sql)
                        self.reader.write_data(sql)

                # Handle `pins` field of the current channel
                if "pins" in entry:
                    pins_list = entry["pins"]
                    sql_list = self.create_list_insert(
                        pins_list, "t_channel_pins", entry["id"], "")
                    for sql in sql_list:
                        self.dprint(sql)
                        self.reader.write_data(sql)

                # Handle `topic` field of the current channel
                topic_dict = entry["topic"]
                topic_dict["parent_id"] = entry["id"]
                sql = self.create_dict_insert(topic_dict, "t_channel_topic")
                self.dprint(sql)
                self.reader.write_data(sql)

                # Handle `purpose` field of the current channel
                purpose_dict = entry["purpose"]
                purpose_dict["parent_id"] = entry["id"]
                sql = self.create_dict_insert(
                    purpose_dict, "t_channel_purpose")
                self.dprint(sql)
                self.reader.write_data(sql)

        self.dprint("Finished open_channels")

    # Writes the given text to the window of the running program
    def dprint(self, text: str):
        if self.max_dprint > -1:
            text = textwrap.shorten(text, width=self.max_dprint)

        self.main_text.insert("1.0", "[{}] {}\n".format(self.count, text))
        self.count += 1
        self.mainframe.update()

    # Closes the program
    def terminate(self):
        print("terminating")
        self.reader.close()
        self.root.destroy()


# Main program execution
if __name__ == '__main__':
    root = Tk()
    print("Tk version = {}, os = {}".format(Tcl().eval(
        'info patchlevel'), root.tk.call('tk', 'windowingsystem')))
    le = Slack2Db(root, "v 3.18.19")
    le.dprint("3.18.19: Added code to link sequential posts")
    le.dprint("3.18.19: Added code to pull down text or grab the preview")
    root.mainloop()
