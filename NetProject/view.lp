/* Objective function */
max: +xS1 +xS2 +xS3 +xS4;

/* Constraints */
+xS1 -x12 -x13 -x14 -x1D = 0;
+xS2 +x12 -x23 -x24 -x2D = 0;
+xS3 +x13 +x23 -x34 -x3D = 0;
+xS4 +x14 +x24 +x34 -x4D = 0;

/* Variable bounds */
xS1 <= 12;
xS2 <= 10;
xS3 <= 13;
xS4 <= 11;
x12 <= 8;
x13 <= 12;
x14 <= 8;
x1D <= 10;
x23 <= 7;
x24 <= 13;
x2D <= 6;
x34 <= 7;
x3D <= 10;
x4D <= 13;
