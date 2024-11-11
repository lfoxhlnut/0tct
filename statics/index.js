// 可配置的API基础路径前缀
// const apiBaseUrl = 'tutorial.localhost:8000/xhl'; // 请替换成你的API基础路径
// 必须以 http(s) 开头
let host = "http://localhost:8000"
let apiBaseUrl = 'xhl'; // 默认API基础路径前缀

// 更新apiBaseUrl的函数
function setApiBaseUrl() {
    let newBaseUrl = document.getElementById('apiBaseUrlInput').value;
    document.getElementById('body-title').innerText = `${newBaseUrl}'s Student Management System`;
    if (!newBaseUrl.startsWith('/')) {
        newBaseUrl = '/' + newBaseUrl
    }
    if (newBaseUrl.endsWith('/')) {
        newBaseUrl = newBaseUrl.slice(0, -1); // 移除末尾的斜杠
    }
    apiBaseUrl = host + newBaseUrl;
    console.log(`API Base URL updated to: ${apiBaseUrl}`);
    // 可以在这里调用getAllUsers或其他函数来使用新的baseUrl
    // getAllUsers();
}

// 绑定按钮点击事件来设置API基础路径
document.getElementById('setBaseUrlButton').addEventListener('click', setApiBaseUrl);

// 辅助函数，用于发送GET请求
// path 要求以 / 开头
function get(path) {
    return fetch(`${apiBaseUrl}${path}`, { method: 'GET' });
}

// 辅助函数，用于发送POST请求
function post(path, data) {
    return fetch(`${apiBaseUrl}${path}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}

// 登录学生
function loginStudent() {
    const studentName = document.getElementById('login-student-name').value;
    const studentId = document.getElementById('login-student-id').value;
    const height = parseFloat(document.getElementById('login-height').value);
    const phone = document.getElementById('login-phone').value;

    return post('/users/login', { student_name: studentName, student_id: studentId, height, phone })
        .then(response => {
            if (response.ok) {
                alert('Login successful');
            } else {
                throw new Error('Login failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 学生登出
function logoutStudent() {
    const studentId = document.getElementById('logout-id').value;

    return get(`/users/logout/${studentId}`)
        .then(response => {
            if (response.ok) {
                alert('Logout successful');
            } else {
                throw new Error('Logout failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 更新学生身高
function updateHeight() {
    const studentId = document.getElementById('update-height-id').value;
    const newHeight = parseFloat(document.getElementById('update-height-value').value);

    return get(`/users/update_height/${studentId}`, { new_height: newHeight })
        .then(response => {
            if (response.ok) {
                alert('Height updated successfully');
            } else {
                throw new Error('Height update failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 检查学生是否在学习
function checkLearning() {
    const studentId = document.getElementById('learning-id').value;

    return get(`/users/learning?id=${studentId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('learning-result').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 获取所有学生信息
function getAllUsers() {
    console.log("in get all users")
    return get('/users/all')
        .then(response => response.json())
        .then(students => {
            const userList = document.getElementById('all-users-list');
            userList.innerHTML = '';
            console.log(students)
            // console.log(JSON.parse(students))
            students.forEach(studentJson => {
                const li = document.createElement('li');
                // content = JSON.parse(studentJson)
                // content = JSON.stringify(studentJson)
                // console.log(content)
                li.innerHTML = `
                <strong>Name:</strong> ${studentJson.student_name}
                <strong>ID:</strong> ${studentJson.student_id}
                <strong>Height:</strong> ${studentJson.height} inches
                <strong>Phone:</strong> ${studentJson.phone}
            `;
                userList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 计算平均身高
function getAverageHeight() {
    return get('/average_height')
        .then(response => response.json())
        .then(data => {
            document.getElementById('average-height-result').innerText = `Average Height: ${data.average_height}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// 获取所有学生信息的函数
// function getAllUsers() {
//     return new Promise((resolve, reject) => {
//         // const eventSource = new EventSource(apiBaseUrl);
//         const eventSource = new EventSource("/event");
//         console.log("connect successfully")
//         eventSource.onmessage = (event) => {
//             const students = JSON.parse(event.data);
//             students.forEach(student => renderStudent(student));
//         };

//         eventSource.onerror = (error) => {
//             console.error('EventSource failed:', error);
//             eventSource.close();
//         };

//         eventSource.onopen = () => {
//             console.log('EventSource connected');
//         };

//         // 存储EventSource实例，以便稍后可以关闭连接
//         window.eventSource = eventSource;
//     });
// }

// 渲染学生信息到页面上的函数
function renderStudent(student) {
    const studentElement = document.createElement('div');
    studentElement.className = 'student';
    studentElement.innerHTML = `
        <p><strong>Name:</strong> ${student.student_name}</p>
        <p><strong>ID:</strong> ${student.student_id}</p>
        <p><strong>Height:</strong> ${student.height} inches</p>
        <p><strong>Phone:</strong> ${student.phone}</p>
    `;
    document.getElementById('students-list').appendChild(studentElement);
}

// 页面加载完成后立即获取所有学生信息
// document.addEventListener('DOMContentLoaded', getAllUsers);

// 绑定点击事件到按钮上
// document.getElementById('login-button').addEventListener('click', loginStudent);
// document.getElementById('logout-button').addEventListener('click', logoutStudent);
// document.getElementById('update-height-button').addEventListener('click', updateHeight);
// document.getElementById('check-learning-button').addEventListener('click', checkLearning);
// // document.getElementById('get-all-users-button').addEventListener('click', getAllUsers);
// document.getElementById('get-average-height-button').addEventListener('click', getAverageHeight);
