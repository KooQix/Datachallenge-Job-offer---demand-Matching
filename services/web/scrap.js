const puppeteer = require("puppeteer");
const fs = require("fs");

const FILE_RES = "services/web/job_qualities.json";

function writeFile(job_name, data) {
	const toWrite = {
		job_name: job_name,
		data: data,
	};
	fs.writeFileSync(FILE_RES, JSON.stringify(toWrite), (err) => {
		if (err) {
			console.log(err);
			return;
		}
	});
}

const _job = process.argv[2];
(async () => {
	if (process.argv.length != 3 || !!!_job) return writeFile("", "");

	const job = _job.toLowerCase();
	const browser = await puppeteer.launch({ headless: true }); //false => open a browser window, true: do it under the hood
	const page = await browser.newPage();
	await page.goto(`https://www.google.com/search?q=${job}+qualit%C3%A9s`);

	//////////////////// Scrapping starts here \\\\\\\\\\\\\\\\\\\\

	const _text = await page.evaluate(() => {
		//////////////////// This will be executed inside the browser, as a user opening the page \\\\\\\\\\\\\\\\\\\\

		try {
			return document.querySelector(".yp1CPe").innerText;
		} catch (error) {
			console.log(`An error occurred while scrapping: ${error}`);
			return null;
		}
	});
	await browser.close();

	// Write job name and description into job_qualities file
	// This file will then be read and the information will be added to the database (done in python)
	if (!!!_text) {
		writeFile(job, "");
		return;
	}

	const text = _text.split("\n\n")[0];
	writeFile(job, text);
})();
