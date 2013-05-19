/* Requires JQuery UI */

function TimeSlider(parent_div_ID, change_function) {
  var me = this; // Disambiguates scope

  this.timerInterval = null;
  this.MAX_VALUE = 23;
  this.MIN_VALUE = 0;
  this.STEP_VALUE = 1;
  this.TIMER_INTERVAL_MILLI = 2000;

  this.change_function = change_function;

  this.parent_div = $("#"+parent_div_ID);

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
      return "12:00 P.M.";
    }
    return "Error";
  }

  this.timeLabel = $(document.createElement("p")).text(getExactTimeLabel(0));
  this.timeLabel.css( {
    "margin-bottom":5,
    "text-align": "center"
  });

  this.slider = $(document.createElement("div")).slider({
      min: me.MIN_VALUE,
      max: me.MAX_VALUE,
      step: me.STEP_VALUE,
      value: me.MAX_VALUE,
      // Change is called when the slider is released and value was changed
      change: function(event, ui) {
        me.timeLabel.text(getExactTimeLabel(me.getSliderValue() + 1));
        if (me.getSliderValue() > me.MAX_VALUE) {
          //Do nothing
        } else {
          if (me.change_function) {
            var num = me.getSliderValue()
            console.log(num);
            me.change_function(num);
          }
          if (me.getSliderValue() === me.MAX_VALUE) {
            me.playButton.attr("src","resources/PlayButton.jpeg");
          } else {
            if (me.timerInterval) {
              me.playButton.attr("src","resources/PauseButton.jpeg");
            } else {
              me.playButton.attr("src","resources/PlayButton.jpeg");
            }
          }
        }
      },
      // Slider is called whenever the slider value is changed
      slide: function(event, ui) {
        //timeLabel.text(slider.slider("value") + ":00");
        if (this.slideFunction) {
          this.slideFunction();
        }
      }
  });
  this.slider.width("95%").css("float","left");

  this.playButton = $(document.createElement("img")).text("Begin Playback").click(function() {
    if (me.timerInterval) {
      // Pause
      clearInterval(me.timerInterval);
      me.timerInterval = null;
      me.playButton.attr("src","resources/PlayButton.jpeg");
    } else {
      //Start Timer
      var slider_value = me.getSliderValue()
      if (slider_value >= me.MAX_VALUE) {
        me.resetSlider();
      }
      me.playButton.attr("src","resources/PauseButton.jpeg");
      me.timerInterval = setInterval(function() {
        var slider_value = me.getSliderValue()
        me.incrementSlider()
        if (me.getSliderValue() >= me.MAX_VALUE) {
          clearInterval(me.timerInterval);
          me.timerInterval = null;
        }
      },me.TIMER_INTERVAL_MILLI);
    }
  }).attr("src","resources/PlayButton.jpeg").width("5%").css("float","right").css("margin-top","-10px").css("max-height", "30px").css("max-width", "30px");
  this.playButton.css("display","inline-block");
  //playButton.css("background-color", "#ff6622");

  this.parent_div.append(this.timeLabel);
  this.parent_div.append(this.slider);
  this.parent_div.append(this.playButton);
  // This final div just allows the last two divs to be floated
  this.parent_div.append($(document.createElement("div")).css("clear","both"));
}

TimeSlider.prototype.getSliderValue = function() {
  return this.slider.slider("value");
}

TimeSlider.prototype.resetSlider = function() {
  this.slider.slider("value",0);
}

TimeSlider.prototype.incrementSlider = function() {
  this.slider.slider("value", this.getSliderValue()+1);
}