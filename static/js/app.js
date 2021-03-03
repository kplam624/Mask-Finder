// Experimental code to save and image to session storage.
// Will use flask to run the smile.py file

var consent = d3.select("#confirm");
var yesButton = consent.select(".yes");

yesButton.on("click", runClick);

function runClick(){
    d3.json("/webcamcapture", function(data){
        var result = data;

        console.log(result);
    })
};

// function runClick(){
//     console.log('I have been clicked.')
// }