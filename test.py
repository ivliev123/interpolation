    for (int i = 0; i < 4; i++) {
        float N_from=N_array[i];
        float QQ = find_points(i,n,N_from);
        Serial.println(QQ);
        Serial.println(N_from);
    }


        //Находим N на каждой кривой, соответствующие выше найденному P, (4 -количество кривых)
    for (int i = 0; i < 4; i++) {
      if (p[i][0] > P) {

        float NN = find_points(i, p, P );
        N_array[i]=NN;
        Serial.println(NN);
        Serial.println(P);
      }
    }
