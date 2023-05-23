const vscode = require('vscode');
const cp = require('child_process');
const path = require('path');
//xesfevcuwbgrellkrcs44tme66yxrosvz3xfjm6nmo3jiqysxkbq
function activate(context) {
	console.log('Congratulations, your extension " api wizard" is now active!');

	let disposable = vscode.commands.registerCommand('API-Wizard.helloWorld', function () {
		const editor = vscode.window.activeTextEditor;
		const selectedText = editor.selection;
		const text = editor.document.getText(selectedText);
		console.log('before spawn ');
		// const pythonProcess = cp.spawn('python', ['../API-Wizard/API_WIzard.py']);
		// const pythonProcess = cp.spawn('python', ['F:/thesis/code/API-Wizard1/API-Wizard/API-Wizard/API_WIzard.py']);
		
		const pythonScriptPath = path.join(__dirname, '..', 'API-Wizard', 'API_WIzard.py');
		const pythonProcess = cp.spawn('python', [pythonScriptPath]);

		console.log('patth curr', __dirname)

		console.log('after spawn and text is ');
		console.log(text);
		pythonProcess.stdin.write(text);
		pythonProcess.stdin.end();
		pythonProcess.stdout.on('data', (data) => {
			console.log('inside python process ');
			const result = data.toString().trim();
			const output = result.split("Output");
			const evaluation = output[1].split("Evaluation");
			console.log(result);

			// Create and show the webview
			const panel = vscode.window.createWebviewPanel(
				'resultView', // Identifies the type of the webview. Used internally
				'API Wizard', // Title of the panel displayed to the user
				vscode.ViewColumn.Two, // Editor column to show the new webview panel in.
				{ enableScripts: true } // Enable scripts in the webview
			);
			panel.webview.html = `<!DOCTYPE html>
			<html lang="en">
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<title>Result</title>
				<style>
					pre {
						white-space: pre-wrap;
						font-size: 1rem;
					}
				</style>
			</head>
			<body>
				<pre>${evaluation[0]}</pre>
			</body>
			</html>`;

			// Handle messages sent from the webview
			panel.webview.onDidReceiveMessage(
				message => {
					if (message.command === 'closeWindow') {
						panel.dispose();
					}
				},
				undefined,
				context.subscriptions
			);

			const channel = vscode.window.createOutputChannel('Result');
			channel.show(true);
			channel.appendLine(output[0]);
			channel.appendLine('Evaluation');
			channel.appendLine(evaluation[1]);

		});

		pythonProcess.stderr.on('data', (data) => {
			console.error(`Python script error: ${data}`);
			vscode.window.showErrorMessage(`Python script error: ${data}`);
		});

		pythonProcess.on('close', (code) => {
			console.log(`Python script process exited with code ${code}`);
		});
	});

	context.subscriptions.push(disposable);
}

function deactivate() { }

module.exports = {
	activate,
	deactivate
}