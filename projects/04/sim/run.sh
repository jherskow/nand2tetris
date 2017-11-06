


# Specify the files to be backed up.
# Below command will backup everything inside the project folder

git add .

# You can also use specific files using the command git add file1 file2 ..
# Committing to the local repository with a message containing the time details

curtime=`date`
git commit -v -m "Automatic Backup @ $curtime" 

# Push the local snapshot to a remote destination

git push origin master

$SHELL



