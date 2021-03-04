// Experimental code to save and image to session storage.
// Will use flask to run the smile.py file

// Defines a function to run on load.

var consent = d3.select("#confirm");
var yesButton = consent.select(".yes");

yesButton.on("click", runClick);


function init(){
    console.log('Hello person.')
    var state = sessionStorage.getItem("result")
    
    switch(state){
        case 'No Mask':

            console.log("Go get a mask");
            
            sessionStorage.removeItem("result");
            break;
        
        case 'Mask':

            console.log("You are free to go in.");
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


init();