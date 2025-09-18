import * as vscode from "vscode";
import * as cp from "child_process";
import * as path from "path";

export function activate(context: vscode.ExtensionContext) {
  console.log("Metadata Viewer extension activated.");

  // supported file types and their associated commands
  const supportedCommands = [
    { ext: ".star", name: "View STAR File", id: "metadataViewer.viewStar", script: "parse_star.py" },
    { ext: ".pkl", name: "View PKL File", id: "metadataViewer.viewPkl", script: "parse_pkl.py" }
  ];

  // register commands for supported file types
  for (const command of supportedCommands) {
    registerViewerCommand(command.ext, command.name, command.id, command.script);
  }

  // auto-launch viewer when a supported file is opened
  // vscode.workspace.onDidOpenTextDocument((doc) => {
  //   if (doc.uri.scheme !== "file") return;

  //   const ext = path.extname(doc.fileName).toLowerCase();
  //   const match = supportedFileTypes.find((f) => f.ext === ext);

  //   if (match) {
  //     // Pass the document URI directly to avoid asking the user
  //     vscode.commands.executeCommand(match.command, doc.uri);
  //   }
  // });

  function registerViewerCommand(
    commandExt: string,
    commandName: string,
    commandId: string,
    commandScript: string
  ) {
    const disposable = vscode.commands.registerCommand(commandId, async (fileUri?: vscode.Uri) => {
      // 1. use fileUri argument if available (usually passed when triggered from explorer context menu)
      // 2. otherwise, prompt user to select a file (fallback)
      if (!fileUri) {
        const inputPath = await vscode.window.showInputBox({
          prompt: `Enter path to ${commandExt} file.`,
          placeHolder: `e.g., /path/to/file${commandExt}`,
          validateInput: (value) => {
            if (!value || !value.endsWith(commandExt)) {
              return `Enter valid ${commandExt} file path.`;
            }
            return null;
          },
        });

        if (!inputPath) {
          vscode.window.showErrorMessage(`${commandName}: No ${commandExt} file selected`);
          return;
        }

        fileUri = vscode.Uri.file(inputPath);
      }
      
      const filePath = fileUri.fsPath;
      const fileName = path.basename(filePath);

      const statusMessageDisposable = vscode.window.setStatusBarMessage(
        `${commandName}: Loading`
      );

      const pythonScript = path.join(context.extensionPath, "python", commandScript);
      const process = cp.spawn("python", [pythonScript, filePath]);

      let stdout = "";
      let stderr = "";

      process.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      process.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      process.on("close", (code) => {
        if (code !== 0 || stderr) {
          statusMessageDisposable.dispose();
          vscode.window.setStatusBarMessage(`${commandName}: Error`, 2000);
          vscode.window.showErrorMessage(`${commandName}: Error parsing ${fileName}: ${stderr || "Unknown error"}`);
          return;
        }

        const tables = stdout
          .split("<<<TABLE_START>>>")
          .slice(1)
          .map((section) => section.split("<<<TABLE_END>>>")[0].trim());

        const html = getHtmlPage(tables);

        statusMessageDisposable.dispose();
        vscode.window.setStatusBarMessage(`${commandName}: Complete`, 2000);

        const panel = vscode.window.createWebviewPanel(
          `${commandExt.replace(".", "").toLowerCase()}Viewer`,
          fileName,
          vscode.ViewColumn.Active,
          { enableScripts: true }
        );

        panel.webview.html = html;
      });
    });

    context.subscriptions.push(disposable);
  }
}

function getHtmlPage(tables: string[]): string {
  const tableHtml = tables.join("");
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {
          font-family: sans-serif;
          padding: 10px;
        }
        table {
          border-collapse: collapse;
          width: 100%;
          margin-bottom: 20px;
        }
        th, td {
          border: 1px solid #ccc;
          padding: 6px 10px;
        }
        th {
          background-color: var(--header-bg);
          color: var(--header-color);
        }
        h3, h2 {
          margin-top: 20px;
        }
        body[data-vscode-theme-kind="vscode-light"] {
          --header-bg: #eee;
          --header-color: #000;
        }
        body[data-vscode-theme-kind="vscode-dark"] {
          --header-bg: #333;
          --header-color: #eee;
        }
        body[data-vscode-theme-kind="vscode-high-contrast"] {
          --header-bg: #000;
          --header-color: #fff;
        }
      </style>
    </head>
    <body>
      ${tableHtml}
    </body>
    </html>
  `;
}

export function deactivate() {}
