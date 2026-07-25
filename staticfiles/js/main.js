(function() {

  clicker = document.getElementById('nav-click')
  nav = document.getElementById('nav')

  function changeState(newState) {
    nav.dataset.state = newState
  }
    
  function toggleState(e) {
    e.preventDefault()
    state = nav.dataset.state
    console.log(state)
    if (state == "hide")
      changeState("show")
    if (state == "show")
      changeState("hide")
  }

  clicker.addEventListener('click', toggleState)
})();