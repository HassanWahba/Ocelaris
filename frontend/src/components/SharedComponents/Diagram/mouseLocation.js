export default {
  methods: {
    getLocation(e) {
      let x = 0;
      let y = 0;
      if (e.touches) {
        x = e.touches[0].pageX;
        y = e.touches[0].pageY;
      } else {
        x = e.pageX;
        y = e.pageY;
      }
      return [x, y];
    }
  }
};
