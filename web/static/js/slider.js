(function() {
  console.log('slider.js')
  slider = document.getElementById('slider')
  nextclick = document.getElementById('next-click')
  prevclick = document.getElementById('prev-click')
  sliderstyles = slider.style
  console.log(sliderstyles.left)


  function next(e) {
    console.log('next slide')
    
    rn_pos = sliderstyles.getPropertyValue('left')
    console.log('rn_pos: '+rn_pos)
    rn_pos = parseInt(rn_pos)
    console.log('rn_pos: '+rn_pos)
    
    new_pos = rn_pos - 100
    console.log('new_pos: '+new_pos)
    if (new_pos < -400)
      new_pos = 0
    slider.style.left = new_pos+'%'
    console.log('final pos: '+sliderstyles.getPropertyValue('left'))
  }
  function prev(e) {
    console.log('prev slide')

    rn_pos = sliderstyles.getPropertyValue('left')
    console.log('rn_pos: '+rn_pos)
    rn_pos = parseInt(rn_pos)
    console.log('rn_pos: '+rn_pos)

    new_pos = rn_pos + 100
    console.log('new_pos: '+new_pos)
    if (new_pos > 0)
      new_pos = -400
    slider.style.left = new_pos+'%'
    console.log('final pos: '+sliderstyles.getPropertyValue('left'))
  }
  whenToSlide = setInterval(next, 15000)
  function pause(e) {
    console.log('paused')
    clearInterval(whenToSlide)
  }
  slider.addEventListener('click', pause)
  nextclick.addEventListener('click', next)
  prevclick.addEventListener('click', prev)
})()