cd /cs/usr/jherskow/HUJI/nand2tetris/projects/10/hardFiles

echo '====FrogGame.xml====' 
java TextComparer ~/test/hardFiles/FrogGame.xml ~/test/hardFiles/FrogGameA.xml

echo '====GameControl.xml====' 
diff -w ~/test/hardFiles/GameControl.xml ~/test/hardFiles/GameControlA.xml
echo '====in3.xml====' 
diff -w  ~/test/hardFiles/in3.xml ~/test/hardFiles/in3A.xml
echo '====simpleCommentTest.xml====' 
diff -w  ~/test/hardFiles/simpleCommentTest.xml ~/test/hardFiles/simpleCommentTestA.xml
echo '====Surface.xml====' 
diff -w  ~/test/hardFiles/Surface.xml ~/test/hardFiles/SurfaceA.xml
echo '====try2.xml===='
diff -w  ~/test/hardFiles/try2.xml ~/test/hardFiles/try2A.xml
