//animation
function onEntry(entry) {
    entry.forEach(change => {
        if (change.isIntersecting) {
            change.target.classList.add('element-show');
        } else if (!change.target.classList.contains('noHidden')) {
            // change.target.classList.remove('element-show');
        }
    });
}

let options = {
    threshold: [0]
};
let observer = new IntersectionObserver(onEntry, options);
let elements = document.querySelectorAll('.element-animation')
for (let elm of elements) {
    observer.observe(elm);
}


//waves
VANTA.WAVES({
    el: ".slide2",
    mouseControls: true,
    touchControls: true,
    gyroControls: false,
    minHeight: 200.00,
    minWidth: 200.00,
    scale: 1.00,
    scaleMobile: 1.00,
    waveSpeed: 0.50
})
//net
VANTA.NET({
    el: ".slide3",
    mouseControls: true,
    touchControls: true,
    gyroControls: false,
    minHeight: 200.00,
    minWidth: 200.00,
    scale: 1.00,
    scaleMobile: 1.00,
    backgroundColor: 0xFFB37D,
    color: 0xf1e0c7,
    points: 7.00,
    maxDistance: 40.00,
    spacing: 20.00
})

//slide1
$.getScript("https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js", function () {
    particlesJS('particles-js',
        {
            "particles": {
                "number": {
                    "value": 50,
                    "density": {
                        "enable": true,
                        "value_area": 500
                    }
                },
                "color": {
                    "value": "#305ae5"
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0,
                        "color": "#000000"
                    },
                    "polygon": {
                        "nb_sides": 5
                    },
                    "image": {
                        "width": 100,
                        "height": 100
                    }
                },
                "opacity": {
                    "value": 0.5,
                    "random": false,
                    "anim": {
                        "enable": false,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 5,
                    "random": true,
                    "anim": {
                        "enable": false,
                        "speed": 40,
                        "size_min": 0.1,
                        "sync": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#2360e5",
                    "opacity": 0.4,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 6,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "attract": {
                        "enable": false,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "repulse"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 400,
                        "line_linked": {
                            "opacity": 1
                        }
                    },
                    "bubble": {
                        "distance": 400,
                        "size": 40,
                        "duration": 2,
                        "opacity": 8,
                        "speed": 3
                    },
                    "repulse": {
                        "distance": 100
                    },
                    "push": {
                        "particles_nb": 4
                    },
                    "remove": {
                        "particles_nb": 2
                    }
                }
            },
            "retina_detect": true,
            "config_demo": {
                "hide_card": false,
                "background_color": "#b61924",
                "background_image": "",
                "background_position": "50% 50%",
                "background_repeat": "no-repeat",
                "background_size": "cover"
            }
        }
    );

});


//scrollpagebutton
function scrollToParagraph(target) {
    const targetParagraph = document.getElementById(target);
    targetParagraph.scrollIntoView({behavior: 'smooth'});
}

//Hide canvas

window.addEventListener('load', function () {
    var canvasElements = document.querySelectorAll('canvas');

    function hideCanvasOnSmallScreens() {
        if (window.innerWidth < 769) {
            canvasElements.forEach(function (canvas) {
                canvas.style.display = 'none';
            });
        } else {
            canvasElements.forEach(function (canvas) {
                canvas.style.display = 'block';
            });
        }
    }

    // Викликати функцію при завантаженні сторінки
    hideCanvasOnSmallScreens();

    // Викликати функцію при зміні розміру вікна
    window.addEventListener('resize', hideCanvasOnSmallScreens);
});
