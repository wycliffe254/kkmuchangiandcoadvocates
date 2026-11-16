(function(){
var b=document.querySelector('.menu'),n=document.getElementById('nav');
if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){n.classList.remove('open');b.setAttribute('aria-expanded','false');b.focus()}})}
var els=document.querySelectorAll('.reveal');
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});els.forEach(function(el){io.observe(el)})}else{els.forEach(function(el){el.classList.add('in')})}
var f=document.getElementById('enquiry');if(!f)return;
var st=document.getElementById('status');
function say(m){st.textContent=m;st.className='status show';st.focus()}
function check(){var ok=true;f.querySelectorAll('[data-req]').forEach(function(i){var e=document.getElementById(i.id+'-err'),m='';
if(!i.value.trim())m='Please complete this field.';
else if(i.type==='email'&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value))m='Please enter a valid email address.';
else if(i.type==='tel'&&i.value&&!/^[+0-9\s()-]{9,16}$/.test(i.value))m='Please enter a valid telephone number.';
else if(i.id==='msg'&&i.value.trim().length<15)m='Please give a little more detail (at least 15 characters).';
e.textContent=m;i.setAttribute('aria-invalid',m?'true':'false');if(m)ok=false});
var c=document.getElementById('consent'),ce=document.getElementById('consent-err');ce.textContent=c.checked?'':'Please confirm that you have read the notice.';if(!c.checked)ok=false;return ok}
f.addEventListener('submit',function(ev){ev.preventDefault();if(!check()){var x=f.querySelector('[aria-invalid=true]');if(x)x.focus();return}
if(f.querySelector('.hp input').value)return;
var url=f.dataset.endpoint;
if(!url){say('This enquiry form is not yet connected to an email service, so nothing has been sent. Please contact the office by telephone, WhatsApp or email using the details on this page.');return}
var btn=f.querySelector('button');btn.disabled=true;
fetch(url,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}}).then(function(r){if(!r.ok)throw 0;f.reset();say('Thank you. Your enquiry has been sent. Submitting it does not create an advocate-client relationship. The office will respond using your preferred contact method.')}).catch(function(){say('Your enquiry could not be sent. Please try again or contact the office directly by telephone or email.')}).then(function(){btn.disabled=false})});
})();
