console.log("start!");
let search = document.getElementsByClassName("btn btn-mini btn-primary uppercase");

search[0].addEventListener("click", () => {
    console.log("click detected!")
    setTimeout(getEmailsFromPage, 1000);
    console.log("here");
//   chrome.scripting.executeScript(tab.id, {
    // code: `(${getEmailsFromPage})();`
//   });
});

// function to get emails
function getEmailsFromPage() {
  let emails = document.getElementsByClassName("results-instructor");
  let professor_name = emails[0].children[0].textContent;
}
