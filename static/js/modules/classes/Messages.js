class Messages {
    STATUS_ERROR = "error"

    constructor(messages_block) {
        this.messages_block = document.querySelector(messages_block)
    }

    render(message, status) {
        let p = document.createElement('p')
        p.classList.add(status)
        p.innerHTML = message
        this.messages_block.append(p)
    }

    clear() {
        this.messages_block.innerHTML = ''
    }

    add_message(data) {
        if (data) {
            let status = data.status || this.STATUS_ERROR
            this.clear()
            if (data.message) {
                this.render(data.message, status)
            } else {
                let keys = Object.keys(data)
                for (let i = 0; i < keys.length; i++)
                    this.render(data[keys[i]], status)
            }
        }
    }
}