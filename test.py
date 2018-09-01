int q[4][4]={{430,665,930,1155},
        {305,510,795,1060},
        {255,375,610,830},
        {125,215,345,475}};
int p[4][4]={{400,300,150,0},
        {203,177,112,0},
        {109,96,65,0},
        {34,31,21,0}};
int n[4][4]={{2675,2350,1905,1550},
        {1935,1825,1660,1470},
        {1405,1345,1260,1140},
        {800,770,730,685}};

float U[]={7.5,6.86,4.58,2.26};

float **points;

//float pxy[][2]={{1,2},{2,4},{3,5},{4,7},{5,3}};


float n_p_abcd[4][4]={};
float p_n_abcd[4][4]={};
float n_q_abcd[4][4]={};
float q_p_abcd[4][4]={};


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


void setup(){
  Serial.begin(9600);
  //int nn =  sizeof(n)/sizeof(int)/(sizeof(n[0])/sizeof(int));
  //Serial.println(nn);


  x = new float [num];
  y = new float [num];

  int  N = sizeof(q)/sizeof(int)/(sizeof(q[0])/sizeof(int)) - 1;

  h = new float [N];
  l = new float [N];
  delta = new float [N];
  _lambda = new float [N];
  c = new float [N];
  a = new float [N];
  b = new float [N];
  d = new float [N];

  c[0] = 0;
  c[N] = 0;


  int num =  sizeof(q)/sizeof(int)/(sizeof(q[0])/sizeof(int));
  points = new float*[num];  // создание строк массива который будет параметром функции spline
  for (int i=0; i<num; i++){
    points[i] = new float[2]; //создание 2-х столбцов для xy
  }


  //
  //int n =  sizeof(pxy)/sizeof(float)/2;
  //закоментировано потому что засоряет память //обьявлена 1 раз в setup
  //  points = new float*[n];  // создание строк массива который будет параметром функции spline
  //  for (int i=0; i<n; i++){
  //    points[i] = new float[2]; //создание 2-х столбцов для xy
  //  }


  // интерполяция P(Q)
  int nni =  sizeof(q)/sizeof(int)/(sizeof(q[0])/sizeof(int));
  int nnj =  sizeof(q[0])/sizeof(int);

  for(int i=0; i<nni; i++){
  for(int j=0; j<nnj; j++){
    points[j][0]=q[i][j];
    points[j][1]=p[i][j];
  }
  spline(points,nnj);  //записывае и выводит в serial значения коэфициентов
//   q_p_abcd[i][0]=a[i];
//  Serial.println(q_p_abcd[i][0]);
  }
  Serial.println();

  // интерполяция P(N)
  //nni =  sizeof(n)/sizeof(int)/(sizeof(n[0])/sizeof(int));
  //nnj =  sizeof(n[0])/sizeof(int);
  for(int i=0; i<nni; i++){
  for(int j=0; j<nnj; j++){
    points[j][0]=n[i][j];
    points[j][1]=p[i][j];
  }
  spline(points,nnj);  //записывае и выводит в serial значения коэфициентов

  }
  Serial.println();

  // интерполяция N(P)
  //nni =  sizeof(p)/sizeof(int)/(sizeof(p[0])/sizeof(int));
  //nnj =  sizeof(p[0])/sizeof(int);
  for(int i=0; i<nni; i++){
  for(int j=0; j<nnj; j++){
    points[j][0]=p[i][j];
    points[j][1]=n[i][j];
  }
  spline(points,nnj);  //записывае и выводит в serial значения коэфициентов
  }
  Serial.println();

  // интерполяция Q(N)
  //nni =  sizeof(n)/sizeof(int)/(sizeof(n[0])/sizeof(int));
  //nnj =  sizeof(n[0])/sizeof(int);
  for(int i=0; i<nni; i++){
  for(int j=0; j<nnj; j++){
    points[j][0]=n[i][j];
    points[j][1]=q[i][j];
  }
  spline(points,nnj);  //записывае и выводит в serial значения коэфициентов
  }
  Serial.println();


  //закоментировано потому что не очищает всю память
  //  for(int i=0; i<n; i++){
  //    delete[]points[i];
  //  }
  //  delete[]points;
  delay(500);


}

void loop(){


}


void spline(float **points,int num){
  //int  N = sizeof(points)/sizeof(float)/2 - 1;
  //num=sizeof(points)/sizeof(float)/2;
  int  N = num - 1;

  for(int i=0; i<num; i++){
    x[i]=points[i][0];
    y[i]=points[i][1];
  }

  for(int i=1; i<N+1; i++){
      h[i] = x[i] - x[i-1];
      l[i] = (y[i] - y[i-1]) / h[i];
    }
  delta[1] = - h[2]/(2 * (h[1] + h[2]));
  _lambda[1] = 1.5 * (l[2] - l[1]) / (h[1] + h[2]);
  for(int i=3; i<N+1; i++){
      delta[i-1] = - h[i] / (2 *h[i-1] + 2 * h[i] + h[i-1] * delta[i-2]);
      _lambda[i-1] = (3 * l[i] - 3 * l[i-1] - h[i-1] * _lambda[i-2]) /(2 * h[i-1] + 2 * h[i] + h[i-1] * delta[i-2]);
    }
    for(int i=N; i>1; i-- ){
        c[i-1] = delta[i-1] * c[i] + _lambda[i-1];
      }

    for(int i=1; i<N+1; i++ ){
        d[i] = (c[i] - c[i-1]) / (3 * h[i]);
        b[i] = l[i] + (2 * c[i] * h[i] + h[i] * c[i-1]) / 3;
        a[i] = y[i];
      }

    for(int i=1; i<N+1; i++ ){
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
