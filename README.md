# Huri-Whakatau-NLP
Huri Whakatau Natural Language Processing back-end GUI  
  
  1. Setup a MySQL database connection with username "root" and password "123456789"
  2. Run the server on localhost
  3. Use the schema.sql in the data directory to setup the database
  4. Run the SlackToDbDHF.py in the src directory
  5. Click on File > Open Users and choose the users.json from the discussion group directory
  6. Click on File > Open Channels and choose the channels.json from the discussion group directory
  7. Click on File > Open Posts and choose one of the topic directories and choose all the .json files in the directory to upload the entire discussion on to the database
  8. Once you upload all the discussions on to the database, run runFile.py in the src directory
  9. The GUI should open and you can then load the discussion on the listbox to explore the text
  10. Click on File > Open Discussion... and navigate to one of the topic directories and select all the files in directory to view the entire discussion on the window
