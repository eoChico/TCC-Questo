function toggleMenu() {
    var navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}
document.addEventListener('DOMContentLoaded', function() {
    showFeature('calendario_fun');
  });
  
  function showFeature(featureId) {
    const features = document.querySelectorAll('.img-fun');
    features.forEach(feature => {
      feature.classList.remove('active');
      if (feature.id === featureId) {
        feature.classList.add('active');
      }
    });
  }

