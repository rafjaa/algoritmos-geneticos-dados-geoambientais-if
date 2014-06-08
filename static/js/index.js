salto = -1;
deslocamento = {'tr01':0,'tr02':0,'tr03':0,'tr54':1600};

resposta = {0:'tr01',1:'tr54',2:'tr03',3:'tr54'};

function $(id)
{
 return document.getElementById(id);
}

$('processar').onclick = function()
{
 proximo();
}

function proximo()
{

 try
 {
  salto++;
 
  $(resposta[salto]).style.zIndex = 100;

  desloca(resposta[salto]);

  setTimeout(proximo,3000);
 }
 catch(err)
 {
  
 } 	
}

function desloca(chave)
{
 try
 {
  $('movimentacao').style.top = -1*deslocamento[chave] + 'px';
 }
 catch(err)
 {
  $('movimentacao').style.top = '0px';
 }
}
