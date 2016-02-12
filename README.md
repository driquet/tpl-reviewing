# Template.py
## Synopsis
Replying the same thing (by mail or any conversation support) multiple times is
quite boring. As a Geocaching Volunteer Reviewer, most of my messages are built
around "templates" (text parts). Several tools exist to facilitate those
repetitive actions, but are not crossplatform or do not meet my expectations.
That is why I decided to create my own tool: **template.py**.

Primarly built for Geocaching Reviewing, this project can be used in other
contexts, where you need to build messages using existing text parts.

## Installation
### Requirements
* requests
* clipboard
* termcolor

You can install these python modules using **pip**:
```
pip install requests clipboard termcolor
```
You may not want to install these packages system-wide. Use **virtualenv** in
that case.

### Clone the repo
```
git clone https://github.com/driquet/tpl-reviewing.git
```

### Edit the configuration file
Use your favorite text editor to customize **review.cfg**. It contains
information to locate file on your filesystem and the url of the spreadsheet
containing templates.

## Writing templates
### Spreadsheet-based tool
At the moment, templates are located in a spreadsheet, formatted in two columns
as follow:
* the first column designate the name of the template
* the second column contains the value of the template

This tool can download a remote csv file containing the template. It is a simple
way to share templates or to distribute easily templates on several computers.
An easy platform is Google Drive, that lets you create spreadsheets that can be
published and shared.

**Todo**: example of spreadsheet

### Boilerplates
A boilerplate is any text that is or can be reused in new contexts or
applications without being greatly changed from the original.

You may want to include a template in another one. For example, if several
templates contain a signature at the end of the text, a smart way to manage the
templates would be to create another template called *signature* and to include
it in those templates. It would be easier to edit your signature only at one
place instead of editing every template involving a signature.

I call this type of template boilerplates.

#### Declaration of a boilerplate
A boilerplate is declared as a template, but its name is surrounded by **[**
and **]**. For example, **[SIGNATURE]**.

#### Using a boilerplate
To include a boilerplate in a template (for example **[SIGNATURE]**), you just need to
use its name in the text of the template. The macro is automatically expanded.
Also, a boilerplate value can contain another boilerplate.

### User input
### User choices
## Usage
The command `python template.py -h` displays a short usage message:
```
usage: template.py [-h] [--config CONFIG] [--refresh] [--reset] [--clipping]
                   [--list]
				   [name]

Template expension process

positional arguments:
	name             Name of the template

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Configuration file
  --refresh, -r    Fetch online the csv to update local template
  --reset          Reset templates score
  --clipping, -c   Copy the result into the clipboard
  --list, -l       List available templates
```
### Refreshing templates
### Listing available templates
### Generating a template
### Reseting templates' score
## Pretty rendering using a fuzzy finder
## TODO
* Support "Drop down" format (template.jar's format)
* Support multiple csv sources
* Support offline version, not based on google spreadsheets

## License
BSD License
