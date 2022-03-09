function countChar(val) {
    var len = val.value.length;
    if (len > 150) {
      val.value = val.value.substring(0, 150);
    } else {
      $('#charNum').text(150 - len);
    }
  };