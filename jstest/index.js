console.log('Doing some js testing')
console.log(window)
var btn = document.getElementById('btn')
let script = document.createElement('script')


btn.addEventListener('click', (e) => {
    e.preventDefault()
    console.log('You clicked the button')
    script.src = 'http://127.0.0.1:5500/jstest/script.js'
    document.head.appendChild(script)
})

document.body.style.background = 'red'

console.log(btn)
console.log(document.head)


// get the varibles

// url
// form fields
// the csrf token

// $.ajax({
//     type: 'POST',
//     // url: url,
//     data : {
//         // the form fields 
//     },
//     success: function(response){
//         console.log(response)
//         document.getElementById('dii')
//     },
//     error: function(error){
//         console.log(error)
//     }
// })