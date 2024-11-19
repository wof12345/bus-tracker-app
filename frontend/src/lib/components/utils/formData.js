export function formData(object = {}) {
    let form = new FormData()

    for (let key in object) {
        form.append(key, object[key])
    }

    return form
}