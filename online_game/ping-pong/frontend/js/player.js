export default class Player {
    constructor(x, y, width, height, color) {
        this.x = x
        this.y = y
        this.width = width
        this.height = height
        this.color = color
        this.score = 0
    }

    draw_l(ctx) {
        ctx.fillStyle = this.color
        ctx.fillRect(this.x, this.y, this.width, this.height)

        // draw score
        ctx.font = "20px Arial"
        ctx.fillText(this.score, 420, this.y < 300 ? 300 - ((this.score.toString().length) * 12) : 325)

        ctx.fillRect(this.x < 400 ? 790 : 0, 0, 10, 500)
    }

    draw_r(ctx) {
        ctx.fillStyle = this.color
        ctx.fillRect(390-this.x, 580-this.y, this.width, this.height)

        // draw score
        ctx.font = "20px Arial"
        ctx.fillText(this.score, 10, this.y < 300 ? 325 : 300 - ((this.score.toString().length) * 12))

        ctx.fillRect(this.x < 400 ? 790 : 0, 0, 10, 500)
    }
}