String cmd;
bool u = 0;
bool d = 0;
bool r = 0;
bool l = 0;

void front(){ //anda 1 bloco para frente
analogWrite(11, 2000);
digitalWrite(9, 1);
digitalWrite(8, 0);
analogWrite(5, 2000);
digitalWrite(7, 0);
digitalWrite(6, 1);
delay(650);
analogWrite(11, 2000);
digitalWrite(9, 0);
digitalWrite(8, 0);
analogWrite(11, 2000);
digitalWrite(7, 0);
digitalWrite(6, 0);
  
}

void rotL(){ //rotaciona para esquerda

analogWrite(11, 2000);
digitalWrite(9, 1);
digitalWrite(8, 0);
analogWrite(5, 2000);
digitalWrite(7, 1);
digitalWrite(6, 0);
delay(500);
analogWrite(11, 2000);
digitalWrite(9, 0);
digitalWrite(8, 0);
analogWrite(11, 2000);
digitalWrite(7, 0);
digitalWrite(6, 0);
  
}

void rotR(){ //rotaciona para direita

analogWrite(11, 2000);
digitalWrite(9, 0);
digitalWrite(8, 1);
analogWrite(5, 2000);
digitalWrite(7, 0);
digitalWrite(6, 1);
delay(500);
analogWrite(11, 2000);
digitalWrite(9, 0);
digitalWrite(8, 0);
analogWrite(11, 2000);
digitalWrite(7, 0);
digitalWrite(6, 0);
  
}
void up(){ //comando de ir para cima

 
  if(u){ //se já estiver indo para cima
    front();//vá para frente
    u = 1; //agora estarás indo para cima
    d = 0;
    r = 0;
    l = 0;
  }
  if(l){ // se estava indo para esquerda
    rotR();//vire a direita
    front();//vá para frente
    u = 1; //agora estarás indo para cima
    d = 0;
    r = 0;
    l = 0;
  }
  if(r){ //se estava indo para direita
    rotL();//vira a esquerda
    front();//vá para frente
    u = 1; //agora estarás indo para cima
    d = 0;
    r = 0;
    l = 0;
  }
}
void down(){
  if(d){
    front();
    u = 0;
    d = 1;
    r = 0;
    l = 0;
  }
  if(r){
    rotR();
    u = 0;
    d = 0;
    r = 1;
    l = 0;
  }
  if(l){
    rotL();
    u = 0;
    d = 0;
    r = 0;
    l = 1;
  }
   
}
void left(){

  analogWrite(11, 2000);
  digitalWrite(9, 1);
  digitalWrite(8, 0);
  delay(2000);
  analogWrite(11, 2000);
  digitalWrite(9, 0);
  digitalWrite(8, 0);
  delay(2000);
  u = 0;
  d = 0;
  r = 0;
  l = 1;
}
void right(){

  analogWrite(11, 200);
  digitalWrite(9, 1);
  digitalWrite(8, 0);
   analogWrite(5, 200);
   digitalWrite(7, 0);
   digitalWrite(6, 1);
  delay(800);
  analogWrite(11, 2000);
  digitalWrite(9, 0);
  digitalWrite(8, 0);
  analogWrite(11, 2000);
  digitalWrite(7, 0);
  digitalWrite(6, 0);
  delay(8000);
  u = 0;
  d = 0;
  r = 1;
  l = 0;
}


void setup() {
  // put your setup code here, to run once:
  pinMode(11, OUTPUT); 
  pinMode(9, OUTPUT); 
  pinMode(8, OUTPUT); 
  pinMode(5, OUTPUT); 
  pinMode(6, OUTPUT); 
  pinMode(7, OUTPUT); 
  Serial.begin(115200);//Python com a mesma boundrate

}

void loop(){

  delay(10000) //espera 10 segundos para colocação no chão
  
  while(Serial.available()==0){ //espera sinal serial
   
  }
  cmd = Serial.readStringUntil('\r'); //lê uma string
  Serial.println(cmd);
  if(cmd=="right"){ //se for para ir a direita
    right();
   
  }
  if(cmd=="up"){ //se for para ir para cima
    up();
   
  }
  if(cmd=="left"){ //se for para ir para esquerda
    left();
  }
  if(cmd=="down"){ //se for para ir para baixo
    down();
   
  }
  
}
