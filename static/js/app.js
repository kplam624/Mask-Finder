// Experimental code to save and image to session storage.
// Will use flask to run the smile.py file

function init(){
    console.log('Hello person.')
    var state = sessionStorage.getItem("result")
    
    switch(state){
        case 'No Mask':
            

            console.log("Go get a mask");

            title.text("You do not have a mask. Please get one.");
            svg.attr('width', 600)
               .attr('height', 600)
               .append('image').attr('xlink:href', noMaskData[index]);


            
            sessionStorage.removeItem("result");
            break;
        
        case 'Mask':

            console.log("You are free to go in.");

            title.text("Thank you! You may now Enter.");
            svg.attr('width', 800)
               .attr('height', 800)
               .append('image').attr('xlink:href', maskData[index]);

            sessionStorage.removeItem("result");
            break;
        
        default:
            console.log('Session Storage is empty.');
    };
};

function runClick(){
    d3.json("/webcamcapture", function(data){
        console.log(data);
        var outcome = data[0].message;

        console.log(outcome);

        sessionStorage.setItem("result", String(outcome));

        location.reload()
    });
};

var noMaskData = data
var maskData = data2
var index = Math.floor(Math.random() * 2)

var consent = d3.select("#confirm");
var yesButton = consent.select(".yes");


var picture = d3.select('#Kevin')

var title = picture.append('h1')
var svg = picture.insert("svg")

// Defines a function to run on load.

yesButton.on("click", runClick);

init();