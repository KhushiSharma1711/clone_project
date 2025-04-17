document.addEventListener("DOMContentLoaded", () => {
  // Auto-hide messages after 5 seconds
  const messages = document.querySelectorAll(".message")
  if (messages.length > 0) {
    setTimeout(() => {
      messages.forEach((message) => {
        message.style.opacity = "0"
        message.style.transition = "opacity 0.5s"
        setTimeout(() => {
          message.remove()
        }, 500)
      })
    }, 5000)
  }

  // Image preview for file inputs
  const fileInputs = document.querySelectorAll('input[type="file"]')
  fileInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const file = this.files[0]
      if (file) {
        const reader = new FileReader()
        const previewContainer = this.parentElement.querySelector(".image-preview")

        if (previewContainer) {
          reader.onload = (e) => {
            previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview">`
          }

          reader.readAsDataURL(file)
        }
      }
    })
  })

  // Textarea auto-resize
  const textareas = document.querySelectorAll("textarea")
  textareas.forEach((textarea) => {
    textarea.addEventListener("input", function () {
      this.style.height = "auto"
      this.style.height = this.scrollHeight + "px"
    })
  })
})

