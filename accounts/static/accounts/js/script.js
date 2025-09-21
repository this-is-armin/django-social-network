const deleteLinks = [
    { id: 'delete_account_link', message: 'Are you sure you want to delete your account?' },
    { id: 'delete_profile_image_link', message: 'Are you sure you want to delete your profile image?' }
];


deleteLinks.forEach(({id, message}) => {
    const link = document.getElementById(id);

    if (link) {
        link.addEventListener('click', (e) => {
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    }
});