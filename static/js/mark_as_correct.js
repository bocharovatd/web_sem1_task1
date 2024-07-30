function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//
// const isCorrectInputs = document.querySelectorAll('.is-correct-input')
//
// for (const isCorrectInput of isCorrectInputs) {
//     isCorrectInput.addEventListener('click', () => {
//         const request = new Request('/mark_as_correct/', {
//             method: 'post',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken')
//             },
//             body: JSON.stringify({
//                 answer_id: isCorrectInput.dataset.answerid,
//             })
//         })
//         fetch(request)
//             .then((response) => response.json())
//     })
// }

function addEventListenersToInput(input) {
    input.addEventListener('click', () => {
        const request = new Request('/mark_as_correct/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                answer_id: input.dataset.answerid,
            })
        });
        fetch(request)
            .then((response) => response.json())
    });
}

const isCorrectInputs = document.querySelectorAll('.is-correct-input');
for (const isCorrectInput of isCorrectInputs) {
    addEventListenersToInput(isCorrectInput);
}
