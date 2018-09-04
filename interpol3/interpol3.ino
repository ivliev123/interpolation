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

float ***n_p_abcd;
float ***p_n_abcd;
float ***n_q_abcd;
float ***q_p_abcd;

float U[] = {7.5, 6.86, 4.58, 2.26};

float **points;

float pxy[][2] = {{1, 2}, {2, 4}, {3, 5}, {4, 7}, {5, 3}};

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

  int num =  sizeof(q) / sizeof(float) / (sizeof(q[0]) / sizeof(float));
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
  n_p_abcd = new float**[num];
  p_n_abcd = new float**[num];
  n_q_abcd = new float**[num];
  q_p_abcd = new float**[num];
  for (int i = 0; i < num; i++) {
    n_p_abcd[i] = new float*[num - 1];
    p_n_abcd[i] = new float*[num - 1];
    n_q_abcd[i] = new float*[num - 1];
    q_p_abcd[i] = new float*[num - 1];
    for (int j = 0; j < num; j++) {
      n_p_abcd[i][j] = new float[4];
      p_n_abcd[i][j] = new float[4];
      n_q_abcd[i][j] = new float[4];
      q_p_abcd[i][j] = new float[4];
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
      spline(points, nnj, q_p_abcd, i); //записывае и выводит в serial значения коэфициентов
    }
    Serial.println();

    // интерполяция P(N)
    for (int i = 0; i < nni; i++) {
      for (int j = 0; j < nnj; j++) {
        points[j][0] = n[i][j];
        points[j][1] = p[i][j];
      }
      spline(points, nnj, n_p_abcd, i); //записывае и выводит в serial значения коэфициентов
    }
    Serial.println();

    // интерполяция N(P)
    for (int i = 0; i < nni; i++) {
      for (int j = 0; j < nnj; j++) {
        points[j][0] = p[i][j];
        points[j][1] = n[i][j];
      }
      spline(points, nnj, p_n_abcd, i);  //записывае и выводит в serial значения коэфициентов
    }
    Serial.println();

    // интерполяция Q(N)
    for (int i = 0; i < nni; i++) {
      for (int j = 0; j < nnj; j++) {
        points[j][0] = n[i][j];
        points[j][1] = q[i][j];
      }
      spline(points, nnj, n_q_abcd, i); //записывае и выводит в serial значения коэфициентов
    }

    Serial.println();
    flag = 0;
  }

  for (int k = 0; k < 4; k++) {
    for (int i = 1; i < 4; i++) {
      Serial.println();
      for (int j = 0; j < 4; j++) {
        Serial.print(q_p_abcd[k][i][j]);
        Serial.print("  ");

      }
    }
    Serial.println();
  }
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
