const todoInput = document.querySelector("#todo-input")
const addBtn = document.querySelector("#add-btn")
const todoList = document.querySelector("#todo-list")

let todos = []

// 미리 저장된 todos가 있는지 확인
const savedTodos = JSON.parse(localStorage.getItem("todos"))

if (savedTodos) {
    todos = savedTodos
    renderTodos()
}

function deleteTodo(index) {
    todos.splice(index, 1)
    renderTodos()
    saveTodos()
}

// 최신 Todo 데이터를 로컬 스토리지에 저장
function saveTodos() {
    localStorage.setItem("todos", JSON.stringify(todos))
}

// 최신 Todo 데이터를 화면에 렌더링
function renderTodos() {
    todoList.innerHTML = ""

    for (const [index, todo] of todos.entries()) {
        const li = document.createElement("li")
        li.className = "list-group-item d-flex justify-content-between align-items-center"
        li.textContent = todo

        const btn = document.createElement("button")
        btn.className = "btn btn-sm btn-danger"
        btn.textContent = "삭제"

        btn.addEventListener("click", () => deleteTodo(index))

        li.appendChild(btn)
        todoList.appendChild(li)
    }
}

function addTodo() {
    const todo = todoInput.value.trim()
    todoInput.value = ""

    if (todo === "") {
        alert("할 일을 입력하세요.")
        return
    }

    todos.push(todo)
    renderTodos()

    // 로컬 스토리지에 저장
    saveTodos()
}

// 할 일 추가
addBtn.addEventListener("click", addTodo)
todoInput.addEventListener("keydown", e => {
    if (e.isComposing) {
        return
    }

    if (e.key === "Enter") {
        addTodo()
    }
})
