const puppeteer = require("puppeteer");
const fs = require("fs");

const FILE_RES = "services/web/job_masc.json";

function writeFile(data) {
	fs.writeFileSync(FILE_RES, data, (err) => {
		if (err) {
			console.log(err);
			return;
		}
	});
}

const _job = process.argv[2];
(async () => {
	if (process.argv.length != 3 || !!!_job) return writeFile("");

	const job = _job.toLowerCase();
	const browser = await puppeteer.launch({ headless: true }); //false => open a browser window, true: do it under the hood
	const page = await browser.newPage();
	await page.goto(`https://www.larousse.fr/dictionnaires/francais/${job}/`);

	//////////////////// Scrapping starts here \\\\\\\\\\\\\\\\\\\\

	const _text = await page.evaluate(() => {
		//////////////////// This will be executed inside the browser, as a user opening the page \\\\\\\\\\\\\\\\\\\\

		try {
			return document.querySelector(".AdresseDefinition").innerText;
		} catch (error) {
			console.log(`An error occurred while scrapping: ${error}`);
			return null;
		}
	});
	await browser.close();

	// Write job name masc
	// This file will then be read and the information will be added to the database (done in python)
	if (!!!_text) {
		writeFile("");
		return;
	}

	try {
		const text = _text
			.split(",")
			.map((element) => element.replace(" ", "").toLowerCase())
			.filter((element) => element !== job)[0];

		writeFile(text);
	} catch (error) {
		writeFile("");
	}
})();
