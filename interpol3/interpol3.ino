
int q[4][4] = {{430, 665, 930, 1155},
  {305, 510, 795, 1060},
  {255, 375, 610, 830},
  {125, 215, 345, 475}
};
int p[4][4] = {{400, 300, 150, 0},
  {203, 177, 112, 0},
  {109, 96, 65, 0},
  {34, 31, 21, 0}
};
int n[4][4] = {{2675, 2350, 1905, 1550},
  {1935, 1825, 1660, 1470},
  {1405, 1345, 1260, 1140},
  {800, 770, 730, 685}
};

float ***abcd;


float U[] = {7.5, 6.86, 4.58, 2.26,0};
float N_array[] = {0, 0, 0, 0};

float Q_array[] = {0, 0, 0, 0, 0};

float **points;

int num;

float *x;
float *y;
float  *h;
float  *l;
float  *delta;
float  *_lambda;

float  *c;
float  *a;
float  *d;
float  *b;

int flag = 1;

void setup() {
  Serial.begin(9600);
  //int nn =  sizeof(n)/sizeof(int)/(sizeof(n[0])/sizeof(int));
  //Serial.println(nn);

  int num = ( sizeof(q) / sizeof(float) ) / ( (sizeof(q[0]) / sizeof(float)));
  x = new float [num];
  y = new float [num];

  h = new float [num];
  l = new float [num];
  delta = new float [num];
  _lambda = new float [num];
  c = new float [num];
  a = new float [num];
  b = new float [num];
  d = new float [num];

  c[0] = 0;
  c[num] = 0;

  points = new float*[num];  // создание строк массива который будет параметром функции spline
  abcd = new float**[num];
  for (int i = 0; i < num; i++) {
    abcd[i] = new float*[num - 1];
    for (int j = 0; j < num; j++) {
      abcd[i][j] = new float[4];
    }
  }
  for (int i = 0; i < num; i++) {
    points[i] = new float[2]; //создание 2-х столбцов для xy

  }
}

void loop() {

  if (flag == 1) {
    int num =  sizeof(q) / sizeof(float) / (sizeof(q[0]) / sizeof(float));

    int nni =  sizeof(q) / sizeof(int) / (sizeof(q[0]) / sizeof(int));
    int nnj =  sizeof(q[0]) / sizeof(int);

    // интерполяция P(Q)
    for (int i = 0; i < nni; i++) {
      for (int j = 0; j < nnj; j++) {
        points[j][0] = q[i][j];
        points[j][1] = p[i][j];
      }
      spline(points, nnj, abcd, i); //записывае и выводит в serial значения коэфициентов
    }
    Serial.println();



    // интерполяция P(N)
    for (int i = 0; i < nni; i++) {
      for (int j = 0; j < nnj; j++) {
        points[j][0] = n[i][j];
        points[j][1] = p[i][j];
      }
      spline(points, nnj, abcd, i); //записывае и выводит в serial значения коэфициентов
    }
    Serial.println();

    int _N = 740;
    int number = 3;

    float P = find_points(number, n, _N );

    Serial.println(_N);
    Serial.println(P);

    // интерполяция N(P)
    for (int i = 0; i < nni; i++) {
      for (int j = 0; j < nnj; j++) {
        points[j][0] = p[i][j];
        points[j][1] = n[i][j];
      }
      spline(points, nnj, abcd, i);  //записывае и выводит в serial значения коэфициентов
    }
    Serial.println();

    //Находим N на каждой кривой, соответствующие выше найденному P, (4 -количество кривых)
    for (int i = 0; i < 4; i++) {
      if (p[i][0] > P) {

        float NN = find_points(i, p, P );
        N_array[i] = NN;
        Serial.println(NN);
        Serial.println(P);
      }
    }

    // интерполяция Q(N)
    for (int i = 0; i < nni; i++) {
      for (int j = 0; j < nnj; j++) {
        points[j][0] = n[i][j];
        points[j][1] = q[i][j];
      }
      spline(points, nnj, abcd, i); //записывае и выводит в serial значения коэфициентов
    }
    Serial.println();

    for (int i = 0; i < 4; i++) { // 4 - количество точек N // нужно заменить (точек межет быть меньше)
      float N_from = N_array[i];
      float QQ = find_points(i, n, N_from);
      Q_array[i]=QQ;
      Serial.println(QQ);
    }

    // интерполяция Q(Uупр)
    
    nni =  sizeof(Q_array) / sizeof(float) ;
    Serial.println(nni);
    for (int i = 0; i < nni; i++) {
        points[i][0] = U[i];
        points[i][1] = Q_array[i];
      }
      spline(points, nni, abcd, 0); //записывае и выводит в serial значения коэфициентов
    
    Serial.println();


    flag = 0;
  }

  //  for (int k = 0; k < 4; k++) {
  //    for (int i = 1; i < 4; i++) {
  //      Serial.println();
  //      for (int j = 0; j < 4; j++) {
  //        Serial.print(abcd[k][i][j]);
  //        Serial.print("  ");
  //
  //      }
  //    }
  //    Serial.println();
  //  }

  delay(10000);
}




void spline(float **points, int num, float ***k_abcd, int nl ) { // nl номер кривой из симейства кривых
  //int  N = sizeof(points)/sizeof(float)/2 - 1;
  //num=sizeof(points)/sizeof(float)/2;
  int  N = num - 1;

  for (int i = 0; i < num; i++) {
    x[i] = points[i][0];
    y[i] = points[i][1];
  }

  for (int i = 1; i < N + 1; i++) {
    h[i] = x[i] - x[i - 1];
    l[i] = (y[i] - y[i - 1]) / h[i];
  }
  delta[1] = - h[2] / (2 * (h[1] + h[2]));
  _lambda[1] = 1.5 * (l[2] - l[1]) / (h[1] + h[2]);
  for (int i = 3; i < N + 1; i++) {
    delta[i - 1] = - h[i] / (2 * h[i - 1] + 2 * h[i] + h[i - 1] * delta[i - 2]);
    _lambda[i - 1] = (3 * l[i] - 3 * l[i - 1] - h[i - 1] * _lambda[i - 2]) / (2 * h[i - 1] + 2 * h[i] + h[i - 1] * delta[i - 2]);
  }
  for (int i = N; i > 1; i-- ) {
    c[i - 1] = delta[i - 1] * c[i] + _lambda[i - 1];
  }

  for (int i = 1; i < N + 1; i++ ) {
    d[i] = (c[i] - c[i - 1]) / (3 * h[i]);
    b[i] = l[i] + (2 * c[i] * h[i] + h[i] * c[i - 1]) / 3;
    a[i] = y[i];
  }

  for (int i = 1; i < N + 1; i++ ) {
    k_abcd[nl][i][0] = a[i];
    k_abcd[nl][i][1] = b[i];
    k_abcd[nl][i][2] = c[i];
    k_abcd[nl][i][3] = d[i];
    Serial.print(a[i]);
    Serial.print("  ");
    Serial.print(b[i]);
    Serial.print("  ");
    Serial.print(c[i]);
    Serial.print("  ");
    Serial.print(d[i]);
    Serial.print("  ");
    Serial.println();
  }
}


int diapazon(float N_val, int array[][4], int num_array) {
  for (int k = 0; k < 4; k++) {
    if (N_val <= array[num_array][k] and N_val >= array[num_array][k + 1] or N_val >= array[num_array][k] and N_val <= array[num_array][k + 1]) {

      return k + 1;
    }
  }
}


float find_points(int num_array, int array[][4], float N_val) {
  int k = diapazon(N_val, array, num_array);


  float xi = array[num_array][k];

  float ai = abcd[num_array][k][0];
  float bi = abcd[num_array][k][1];
  float ci = abcd[num_array][k][2];
  float di = abcd[num_array][k][3];

  float Y = ai + bi * (N_val - xi) + ci * pow((N_val - xi), 2) + di * pow((N_val - xi), 3);
  return Y;
}
