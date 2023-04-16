function fetchForm() {
    window.open("/form", "", "toolbar=no");
}


function viewInput() {
    if (document.getElementById("userInput").style.display === "none") {
        const xmlhttp = new XMLHttpRequest();
        xmlhttp.onload = function () {
            data = JSON.parse(this.responseText);
            document.getElementById("name").innerHTML = data["name"];
            document.getElementById("gender").innerHTML = data["gender"];
            document.getElementById("birthyear").innerHTML = data["birthyear"];
            document.getElementById("birthplace").innerHTML = data["birthplace"];
            document.getElementById("residence").innerHTML = data["residence"];

            for (let i = 1; i <= 20; i++) {
                const question = document.getElementById(`q${i}`);
                const answer = data["question"][i];
                question.innerHTML += "[" + answer + "]";
            }

            document.getElementById("job").innerHTML = data["job"];
            document.getElementById("pets").innerHTML = data["pets"];
            document.getElementById("message").innerHTML = data["message"];
        }

        xmlhttp.open("GET", "view/input", true);
        xmlhttp.send();
        document.getElementById("userInput").style.display = "block";
    }

    else {
        document.getElementById("name").innerHTML = "";
        document.getElementById("gender").innerHTML = "";
        document.getElementById("birthyear").innerHTML = "";
        document.getElementById("birthplace").innerHTML = "";
        document.getElementById("residence").innerHTML = "";

        for (let i = 1; i <= 20; i++) {
            const question = document.getElementById(`q${i}`);
            question.innerHTML = "";
        }

        document.getElementById("job").innerHTML = "";
        document.getElementById("pets").innerHTML = "";
        document.getElementById("message").innerHTML = "";
        document.getElementById("userInput").style.display = "none";
    }
}


function viewProfile() {
    if (document.getElementById("userProfile").style.display === "none") {
        const xmlhttp = new XMLHttpRequest();
        xmlhttp.onload = function() {
            data = JSON.parse(this.responseText);
            document.getElementById("psyc").innerHTML = data["psycho"]["psyc_index"];
            document.getElementById("desiredJob").innerHTML = data["career"]["desired"];
            document.getElementById("suitability").innerHTML = data["career"]["suitability"];
            document.getElementById("movieTitle").innerHTML = data["movies"]["title"];
            document.getElementById("movieYear").innerHTML = data["movies"]["year"];
            document.getElementById("movieRuntime").innerHTML = data["movies"]["runtime"];
            document.getElementById("movieGenre").innerHTML = data["movies"]["genre"];
            document.getElementById("movieDirector").innerHTML = data["movies"]["director"];
            document.getElementById("movieActors").innerHTML = data["movies"]["actors"];
            document.getElementById("movieRating").innerHTML = data["movies"]["rating"];

            if (data["pets"] !== undefined) {
                const canvas = document.getElementById("petCanvas");
                const context = canvas.getContext("2d");
                context.clearRect(0, 0, 1000, 1000);
                let i = 0;
                for (const pet in data["pets"]) {
                    const img = new Image();
                    img.onload = () => {
                        context.drawImage(img, 10 + (i * 250), 10, 250, 250);
                        i++;
                    };
                    img.src = "view/" + pet;
                }
            }
        }

        xmlhttp.open("GET", "view/profile", true);
        xmlhttp.send();
        document.getElementById("userProfile").style.display = "block";
    }

    else {
        document.getElementById("psyc").innerHTML = "";
        document.getElementById("desiredJob").innerHTML = "";
        document.getElementById("suitability").innerHTML = "";
        document.getElementById("movieTitle").innerHTML = "";
        document.getElementById("movieYear").innerHTML = "";
        document.getElementById("movieRuntime").innerHTML = "";
        document.getElementById("movieGenre").innerHTML = "";
        document.getElementById("movieDirector").innerHTML = "";
        document.getElementById("movieActors").innerHTML = "";
        document.getElementById("movieRating").innerHTML = "";
        const canvas = document.getElementById("petCanvas");
        const context = canvas.getContext("2d");
        context.clearRect(0, 0, 1000, 1000);
        document.getElementById("userProfile").style.display = "none";
    }
}