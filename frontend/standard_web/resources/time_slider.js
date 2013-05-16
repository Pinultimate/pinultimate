/* Requires JQuery UI */

var createTimeSlider = function(divID,changeFunction,slideFunction) {

  var me = this; // Disambiguates scope

  me.timerInterval = null;
  me.MAX_VALUE = 23;
  me.MIN_VALUE = 0;
  me.STEP_VALUE = 1;
  me.TIMER_INTERVAL_MILLI = 3000;

  var parentDiv = $("#"+divID);
  
  var getExactTimeLabel = function(offset) {
    var date = new Date();
    var hours = date.getHours();

    // Get Appropriate Day
    var month = date.getMonth()+1;
    var day = date.getDate();
    var month_day_formatted = month + "/" + day;
    var full_time_string = month_day_formatted;
    time = hours + offset;
    if (time >= 24) {
      time -= 24;
    }
    if (time === 0) {
      return "12:00 A.M.";
    }
    if (time < 12) {
      return time + ":00 A.M.";
    } else if (time > 12) {
      return (time-12) + ":00 P.M.";
    } else { // time === 12
      return "12:00 PM";
    }
    return "Error";
  }

  // Create time label
  var timeLabel = $(document.createElement("p")).text(getExactTimeLabel(0));
  timeLabel.css( {
    "margin-bottom":5,
    "text-align": "center"
  });
  // Create slider
	var slider = $(document.createElement("div")).slider({
      min: this.MIN_VALUE,
      max: this.MAX_VALUE,
      step: this.STEP_VALUE,
      value: this.MAX_VALUE,
      // Change is called when the slider is released and value was changed
      change: function(event, ui) {
        timeLabel.text(getExactTimeLabel(slider.slider("value") + 1));
        if (changeFunction) {
          var num = slider.slider("value");
          console.log(num);
          changeFunction(num);
        }
      },
      // Slider is called whenever the slider value is changed
      slide: function(event, ui) {
        //timeLabel.text(slider.slider("value") + ":00");
        if (slideFunction) {
          slideFunction();
        }
      }
  });
  slider.width(900);
  slider.css("float","left");

  var playButton = $(document.createElement("div")).text("play")
  playButton.click(function() {
    console.log("Clicked!");
    if (me.timerInterval) {
      // Pause
      clearInterval(me.timerInterval);
      me.timerInterval = null;
      playButton.html("play");
    } else {
      //Start Timer
      var slider_value = slider.slider("value");
      if (slider_value >= MAX_VALUE) {
        // Start Playback
        slider.slider("value",0);
      }
      playButton.text("pause");
      me.timerInterval = setInterval(function() {
        console.log("timer set");
        var value = slider.slider("value");
        if (value >= MAX_VALUE) {
          clearInterval(me.timerInterval);
          me.timerInterval = null;
          playButton.html("play");
        }
        slider.slider("value",value+1);
      },me.TIMER_INTERVAL_MILLI);
    }
  });

  playButton.css("float","right");
  //playButton.css("background-color", "#ff6622");

  parentDiv.append(timeLabel);
  parentDiv.append(slider);
  parentDiv.append(playButton);
  // This final div just allows the last two divs to be floated
  parentDiv.append($(document.createElement("div")).css("clear","both"));
}