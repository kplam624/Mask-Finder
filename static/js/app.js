// Experimental code to save and image to session storage.
// Will use flask to run the smile.py file

function init(){
    // This function is responsible for the message posted, based on the outcomes of the model.
    // console.log('Hello person.');

    // Pulls the result and defines which image is used.
    var state = sessionStorage.getItem("result");
    var index = Math.floor(Math.random() * 2);

    // Resets the title and the svg elements.
    var removeTitle = picture.selectAll('h1')
                             .remove();
    var removeSvg = picture.selectAll('svg')
                             .remove();
    
    // Using switch statements to define how the page looks.
    switch(state){
        // First case
        case 'No Mask':
            // console.log("Go get a mask");

            // Creates the title and the image associated with it.
            var title = picture.append('h1');
            var svg = picture.insert("svg");

            // Populates the title element and the image element.
            title.text("You do not have a mask. Please get one.");
            svg.attr('width', 600)
               .attr('height', 600)
               .append('image').attr('xlink:href', noMaskData[index]);

            // Clears the session storage.
            sessionStorage.removeItem("result");
            break;
        
        // Second case
        case 'Masked':
            // console.log("You are free to go in.");

            // Creates the title and the image associated with it.
            var title = picture.append('h1');
            var svg = picture.insert("svg");

            // Populates the title element and the image element.
            title.text("Thank you! You may now Enter.");
            svg.attr('width', 700)
               .attr('height', 500)
               .append('image').attr('xlink:href', maskData[index]);

            // Clears the session storage.
            sessionStorage.removeItem("result");
            break;
        
        // The default case.
        default:
            console.log('Session Storage is empty.');
    };
};

// A function that does a 'GET' request on the flask server.
function warning(){
    // Pulls the information as a json file.
    d3.json("/webcamcapture", function(data){

        // console.log(data);

        // Creates a variable called outcome to store in a session storage
        var outcome = data[0].message;
        // console.log(outcome);

        // Stores the string to be used for the init()
        sessionStorage.setItem("result", String(outcome));

        init();
    });
};

// To set up the data needed for possible outcomes
var noMaskData = data;
var maskData = data2;

// var index = Math.floor(Math.random() * 2)

// Using d3 to later create event listeners.
var consent = d3.select("#confirm");
var yesButton = consent.select(".yes");

// Using d3 to create titles and images.
var picture = d3.select('#Kevin');

// Defines a function to run on load.
init();