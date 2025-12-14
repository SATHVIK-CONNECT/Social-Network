function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function activateFocus(post_id) {
  const btn = document.getElementById(`text_${post_id}`);
  setCursor(btn);
}

function setCursor(btn) {
  btn.focus();
  const btn_length = btn.value.length;
  btn.setSelectionRange(btn_length, btn_length);
}

function editOption(post_id) {
  const btn = document.getElementById(`edit_option_${post_id}`);
  const editor = document.getElementById(`text_${post_id}`);
  const saver = document.getElementById(`save_${post_id}`);
  const original_content = document.getElementById(`content_${post_id}`);
  btn.style.display = "none";
  editor.style.display = "block";
  saver.style.display = "block";
  original_content.style.display = "none";
}

function saveContent(post_id) {
  const btn = document.getElementById(`edit_option_${post_id}`);
  const editor = document.getElementById(`text_${post_id}`);
  const saver = document.getElementById(`save_${post_id}`);
  const original_content = document.getElementById(`content_${post_id}`);
  const editor_content = editor.value;
  btn.style.display = "block";
  editor.style.display = "none";
  saver.style.display = "none";
  original_content.style.display = "block";

  fetch(`/editPost/${post_id}`, {
    method: "POST",
    headers: { "Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
    body: JSON.stringify({
      content: editor_content,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      original_content.innerHTML = result.data;
    });
}

async function likes(postId, likedUsers) {
  const isLiked = likedUsers.includes(postId);
  const url = isLiked ? `/removingLike/${postId}` : `/addingLike/${postId}`;
  const likeButton = document.getElementById(`${postId}`);

  try {
    const response = await fetch(url);
    const data = await response.json();
    const likeCount = data.count;
    if (isLiked) {
      likeButton.classList.remove("fa-solid");
      likeButton.classList.add("fa-regular");
    } else {
      likeButton.classList.remove("fa-regular");
      likeButton.classList.add("fa-solid");
    }

    const likeCountElement = document.getElementById(`like_count_${postId}`);
    likeCountElement.textContent = likeCount;
  } catch (error) {
    console.error("Error fetching like count:", error);
  }
}
