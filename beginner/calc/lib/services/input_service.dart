class InputService {
  static String handleInput(String currentValue, String input) {
    // Handle clear functions
    if (input == 'C') {
      return '0';
    }
    
    if (input == 'CE') {
      return '0';
    }
    
    // Handle sign change
    if (input == '+/-') {
      if (currentValue == '0') {
        return '0';
      }
      if (currentValue.startsWith('-')) {
        return currentValue.substring(1);
      } else {
        return '-$currentValue';
      }
    }
    
    // Handle decimal point
    if (input == '.') {
      if (currentValue.contains('.')) {
        return currentValue; // Already has decimal point
      }
      if (currentValue == '0') {
        return '0.';
      }
      return '$currentValue.';
    }
    
    // Handle digit input
    if (currentValue == '0' && input != '.') {
      return input;
    }
    
    // Limit to 8 digits
    if (currentValue.length >= 8) {
      return currentValue;
    }
    
    return '$currentValue$input';
  }
}