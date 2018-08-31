
float **points;

float pxy[][2]={{1,2},{2,4},{3,5},{4,7},{5,3}};

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
  num=sizeof(pxy)/sizeof(float)/2; //количество элементов массива points
  x = new float [num];
  y = new float [num];

  int  N = sizeof(pxy)/sizeof(float)/2 - 1;

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

//  int n =  sizeof(pxy)/sizeof(float)/2;
// 
//  points = new float*[n];  // создание строк массива который будет параметром функции spline
//  for (int i=0; i<n; i++){
//    points[i] = new float[2]; //создание 2-х столбцов для xy
//  }
}

void loop(){

  //
  int n =  sizeof(pxy)/sizeof(float)/2;
 // float **points;
  points = new float*[n];  // создание строк массива который будет параметром функции spline
  for (int i=0; i<n; i++){
    points[i] = new float[2]; //создание 2-х столбцов для xy
  }
  
  for(int i=0; i<n; i++){
    points[i][0]=pxy[i][0];
    points[i][1]=pxy[i][1];
  }
  spline(points,n);  //записывае и выводит в serial значения коэфициентов

  
  for(int i=0; i<n; i++){
    delete[]points[i];
  }
  delete[]points;
  delay(100);
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
        Serial.println(a[i]);
        Serial.println(b[i]);
        Serial.println(c[i]);
        Serial.println(d[i]);
        Serial.println();
      }

     
}

