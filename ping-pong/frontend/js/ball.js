export default class Ball {
    constructor(x, y, radius, color) {
        this.x = x
        this.y = y
        this.radius = radius
        this.color = color
    }

    draw_l(ctx) {
        ctx.fillStyle = this.color
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
        ctx.fill();
    }

    draw_r(ctx) {
        ctx.fillStyle = this.color
        ctx.beginPath();
        ctx.arc(450-this.x, 600-this.y, this.radius, 0, 2 * Math.PI);
        ctx.fill();
    }
}