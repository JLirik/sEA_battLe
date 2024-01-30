curTab = 0;
showTab();

function showTab(){
	var x = document.getElementsByClassName('tab');
	x[curTab].style.display = 'block'
	if(curTab == 0){
		document.getElementById('prev').style.display = 'none'
	}
	else{
		document.getElementById('prev').style.display = 'inline'
	}
	if(curTab == x.length - 1){
		document.getElementById('next').innerHTML = 'Отправить'
	}
	else{
		document.getElementById('next').innerHTML = 'Следующий шаг'
	}
	stepIndicator()
}
function moveTab(n){
	var x = document.getElementsByClassName('tab')
	if(n == 1 && !validateForm()){
		return false
	}
	x[curTab].style.display = 'none'
	curTab = curTab + n
	if(curTab >= x.length){
		document.getElementById('form').submit()
		return false
	}
	showTab()
}
function validateForm(){
	var tab, input, valid = true, a;
	tab = document.getElementsByClassName('tab');
	input = tab[curTab].getElementsByTagName('input');
	for(i=0; i<input.length; i++){
		if (input[i].value == '' && input[i].name != 'admin'){
			valid = false;
			input[i].className += ' invalid';
		}
		else if (input[i].name == 'email' && (input[i].value.indexOf('@') == -1 || input[i].value.indexOf('.') == -1)){
		    alert('Бро, почта написана неправильно, кажись @ или . забыл :)')
			valid = false;
			input[i].className += ' invalid';
		}
	}
	if (valid){
		document.getElementsByClassName('step')[curTab].className += ' finish'
	}
	return valid
}
function stepIndicator(){
	var x = document.getElementsByClassName('step')
	for(i=0; i<x.length; i++){
		x[i].className = x[i].className.replace(" active", '')
	}
	x[curTab].className += ' active'
}
