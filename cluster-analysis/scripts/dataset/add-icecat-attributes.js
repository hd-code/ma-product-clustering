(async function() {
    async function sleep(ms) {
        return new Promise(resolve => {
            setTimeout(() => {resolve()}, ms)
        })
    }

    add_btn = document.querySelector(".src-containers-search-box-style__orangeButton--2Hbxm")

    add_btn.click()
    await sleep(2000)
    alert("Hallo Welt")
})()
