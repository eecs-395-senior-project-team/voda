import debug from 'debug';

class Log {
  constructor() {
    this.BASE = 'voda';
    this.COLOURS = {
      info: 'blue',
      error: 'red',
    };
  }

  generateMessage(level, message, source) {
    // Set the prefix which will cause debug to enable the message
    const namespace = `${this.BASE}:${level}`;
    const createDebug = debug(namespace);

    // Set the colour of the message based on the level
    createDebug.color = this.COLOURS[level];

    if (source) {
      createDebug(source, message);
    } else { createDebug(message); }
  }

  info(message, source) {
    return this.generateMessage('info', message, source);
  }

  error(message, source) {
    return this.generateMessage('error', message, source);
  }
}

export default new Log();
