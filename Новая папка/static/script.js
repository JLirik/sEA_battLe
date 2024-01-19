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
		document.getElementById('next').innerHTML = 'Finish'
	}
	else{
		document.getElementById('next').innerHTML = 'Next step'
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
	var tab, input, valid = true;
	tab = document.getElementsByClassName('tab');
	input = tab[curTab].getElementsByTagName('input');
	for(i=0; i<input.length; i++){
		if (input[i].value == ''){
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