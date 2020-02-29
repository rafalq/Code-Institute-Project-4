[![Build Status](https://travis-ci.com/rafalq/Code-Institute-Project-4.svg?token=qAUnRqnak3C9xDgqZxRq&branch=master)](https://travis-ci.com/rafalq/Code-Institute-Project-4)

# Project 4 - Auction Store

Code Institute - Full Stack Frameworks with Django Milestone Project.

## Project Idea:  

### Build an auction place to sell historical artifacts.

This is my auction store website which is the last Milestone Project in the Fullstack Web Developer course.

It is focused on both Front End and Back End Development skills. 

I used one of the ideas provided on the course website. It is a brand new Django project composed of multiple apps.

Artifa is a fictitious online auction store. All selling items are unique historical artifacts. The store has its own collection for sale but registered users can also sell their items.

Sellers and buyers have two options except of sale they can use auction. This way they can bid or put up artifacts for auction. Popularity of ebay explains that this kind of online stores can be extremely successful. 

By choosing auction, there is also possibility to buy an artifact for a fixed price. This benefits both the user and the store. The former omits the whole process if they are interested in this specific item to purchase, the latter sells the item for the price they wanted to.

I tried to create the website as much user friendly as possible. The payment form uses the user's profile personal details for the delivery address so that they do not have to fill it in if they have already provided their address there. They can also see their history activity. This way they can easily find the last item they bid, the item they put up for sale or their purchases. The cart and the history is updated after every change what can be easily noticed.

The target audience is everyone who has passion for history and is a collector of that kind of items.


## UX

### User Stories

User 1 looks for an artifact to buy.

User 2 wants to sell an item or put up it for auction.

User 3 wants to participate in an auction or buy an item for the set price.

User 4 wants to find the item they have bid or sold or bought recently.

User 5 wants to buy artifacts that they won at auctions.

User 6 wants to update some details of their selling items or their account.

### Strategy

The goal was to create a website for existing and potential customers in order to sell and bid artifacts, manage store online and to promote the brand.

### Scope

User 1 can find any item available for sale in the store using the search bars on the store page.

User 2 can fill in the `For Sale` form to sell their artifacts or put them up for auction after they sign up.

User 3 Both options are available on the item page if the user is registered. 

User 4 can view their history page anytime. The latest activity is being noticeably indicated. 

User 5 can find all the artifacts won at auction in their cart.

User 6 can update the above easily.

### Structure

The website consists of two applications and the following pages:

#### Auction Store Application

__base.html__ 

The webpage is extended by the rest pages. It contains the navigation bar which includes links to appropriate parts of the website;  some of them are only available after signing in.

__home.html__

This is an entry webpage of the website. It is divided into five sections and contains any updates done by the store. There are also the `About ` section and the` Contact` one where you find a message form.

__store.html__

The main page.  You can find all available artifacts for sale here. The page is paginated. The navbar contains a search bar. You can make individual adjustment to the search using the dropdown box on the left side. All the selling formats are marked by appropriate icons on the items.


#### Pages available only after login

__item_detail.html__

The website is an actual item description. It contains more detailed information about the item and two buttons, one for bidding, the other for buying or if the item is being selling by the logged user - an update button and a delete button. The modal is used for bidding option. On the right side there is a bid section contains: the progress bar indicating the time left to the end of the auction, the start and the end date, the initial bid, and all the auction bids placed vertically.

__create_form.html__

Users can get there by clicking the `ad` icon in the navigation bar. If a user wants to sell an artifact, they use the form to do this. The webpage is a blank form contains titled input fields and `Submit` button.  

__item_form.html__

When a user clicks the update button on the item's page, they are directed to a form including the filled-in fields that can be modified. There is also a submit button at the bottom of the page.

__item_confirm_delete.html__

When a user clicks the delete button on the item's page, they are directed to a webpage including the two buttons: one for cancelling the delete operation, the other for confirmation.

__payment.html__

A payment form including a delivery address fields plus stripe-styled payment field.  A button below for `Submit`.


#### Users Application 

__register.html__

You can register your account to use application buying, bidding and selling options. By clicking the register link right side of the bar, you are taken to a webpage containing a registration form. Only four fields are required for the process.  

__login.html__

Registered users can log in to be able to use all the options available on the website. The page contains a username field and a password field. If someone forgets their password, they can use `Forget Password` link which directs them to another webpage or if an account is needed, they can use another link to register.

__password_reset.html__, 
__password_reset_confirm.html__, 
__password_reset_confirm.html__, 
__password_reset_complete.html__

Webpages contains forms and buttons or messages and links referring to a password reset process.


#### Pages available only after login

__cart.html__

The webpage shows all artifacts won by the user during auctions. They are placed horizontally just below the `navbar`. If there more than one of them, a scroll bar can be used for viewing. All item details are placed inside a bootstrap card.

__profile.html__
When a user clicks the portrait icon on the` navbar`, they are directed to a form including the filled-in fields with the user personal details that can be modified.

__history.html__
The page contains a search bar and three columns that display information about purchasing, selling and bidding. Each column has a sort bar at the top.

__logout.html__
The page displays a message: `You have been logged out`.


### Colors

All used color are of bootstrap origin. The main ones are: primary, warning, danger, dark and blend of them. They seem to create a pleasant contrast between each other. 

## Technologies

1. Django (2.1.7)
2. Javascript
3. jQuery (3.4.1)
4. Bootstrap (4.3.1)
5. HTML5
6. CSS3


## Features

* Contact option enabling users to communicate with the store online
* User registration and authentication

### Registered Users

* Resetting password
* Updating account details
* Viewing the history of own activity
* Searching the history through items by names and to sort it by date or price
* Viewing the cart which contains items won at auction
* Putting an item for sale or auction, update and delete it

### The Store

* Searching through items by name, category, price, format and seller or a combination of any of those
* Sorting the items by date or price
* Pagination (five artifacts per page)
* Statistics showing how many items match search criteria

### The Item Pages

* Buying for the set price or bid the item
* Updating or deleting the item by the seller
* Viewing detailed information about the item specification, delivery and their histories ("Read more" link can be added only for items selling by the store)
* Viewing and following an auction time (a progress bar was used as a timer, available only for Chrome browser)
* Viewing a bid history 
* Bidding quicker by using set in advance prices buttons  

### Payment

* Paying card 
* Using the account information as the delivery address

## Testing

The website can be open with the browsers:  
`Firefox (Version 70.0.1`), 
`Opera (Version 63.0.3)`, 
`Internet Explorer (Version 11.0.9)`, 
`Google Chrome (Version 77.0.3`);
The responsiveness was checked in Chrome Development Tools.

### Frontend

 __HTML__
 
 [W3C Markup Validation](https://validator.w3.org/) was used to validate HTML.

 __CSS__
 
 [W3C CSS validation](https://jigsaw.w3.org/css-validator/) was used to validate CSS.

The rest tests were run manually.
	
Click the logo and verify being redirected to home page.

Click the `Home` link and verify being redirected to home page.

Click the `About` link and verify being redirected to the `About` section on the home page.

Click the `Store` link and verify being redirected to the store.html page.

Click the `Contact` link and verify being redirected to the `Contact` section on the home page.
	
Click the `Login` link and verify being redirected to the `login.html` page.

Click the `Register` link and verify being redirected to the `register.html` page.


Log in and hover over each icons in the right side of the `navbar`, verify if they display (starting from the left): `Sell`, `Account`, `History`, `Cart`.

Click the `Sell` icon and verify being redirected to the `create_form.html` page.

Click the `Account` icon and verify being redirected to the `create_form.html` page.

Click the `History` icon and verify being redirected to the `history.html` page.

Click the `Cart` icon and verify being redirected to the `cart.html` page.

Click the `Home` link and then the left and the right carousel button.

Click the `Home` link and then the `Shop Now` button in the middle of the page and verify being redirected to the `store.html` page.

Log in, click the `Store` link and then click anyone of item titles available on the page,
verify being redirected to the `item_detail.html` page.

On the above page click the Place Bid button and verify if a modal comes up.
Press each of the buttons available there and verify if they are working, then click the `Cancel` button in the top right corner of the modal.
On the same page as above click the `Buy Now` button and verify being redirected to the `payment.html` page.

On the payment page click the name of the item and verify being redirected to this `item_detail.html` page.
	
 __Javascript__
 
All tests were run manually.

Go to the `Contact` section on the home page and type an email address without "@", verify that an error message appears.
In the same section, leave one of the fields blank and press the Send button, verify that an error message appears.

Log in, got to the `store.html` page and then go to one of the items page. Verify that the progress bar and the numeric-style clock are working accurately. Refresh the page; check if the progress of the progress bar was not reset (only in `Chrome`).

Log in, got to the `store.html` and then go to one of the items page containing the `Buy Now` button. Click this and on the `payment.html` at the bottom of the form, type for the card number a number different than the [Basic test card numbers](https://stripe.com/docs/testing)
Verify that an error message appears.
Repeat the same for the expiry month and the year, typing this time some older date than today.

Log in, go to your history. If there is any activity displaying one of the table, type in the search bar the title or the date or the price. Verify that only those items are displaying and the rest removed. 
If there are more than one item in a column, sort them using the sort option. Verify if that work correctly for each category.
	
In the search table, sort the items by their format choosing the `Auction`. Verify that the progress bar and the numeric-style clock are working accurately. Refresh the page; check if the progress of the progress bar was not reset.
	

### Backend

#### Django  

All tests for the backend were run manually.

##### Login / Registration / Password Reset

Log in with an unregistered username and password, verify that an error message appears.
Log in with a registered username but wrong password; verify an error message is displayed.
Log in with a registered username and correct password; verify being redirected to the `store.html` page.
Close the page and open it again, verify the user is still logged in.
Log out, verify being redirect to the `logout.html` page. Refresh the page and check if you are still logged out.
	
Register with a username already being used; verify an error message is displayed.
Register with a email address without "@" and ".", verify an error message is displayed.
Register with a password confirmation different than the password; verify an error message is displayed.
Click the `Sign In` link at the bottom of the above form page and verify being taken to the `login.html` page.

On the page click the `Register Now` link at the bottom and verify being taken to the `register.html` page.

Go back to the page and click the `Forgot Password?` link at the bottom and verify being taken to the `password_reset.html` page.

Type your correct email address, click the button and verify being redirect to the page with the message stating `An email has been sent with instructions to reset your password!`. 
Click the `Go Back to Store` link. You should be taken to the `store.html` page.
Now check your email box and find a message with a link for resetting your password. 
Click it. Verify being redirect to the `password_reset_confirm.html`.

Type your new password and the same for the new password confirmation. You should be taken to the `password_rest_complete`  page. Click the `Sign In Here` link below the message. Verify being taken to the `login.html` page. From here use a new password and verify that you can log in.

##### Searching Option / Pagination
Log in, go to your History. Check if there is any item in it. If so, type one of their titles in the search field and check if only this one appears.

On the same page, if there is more than one item, try to sort each category. Repeat the sequence for all columns. Verify it works correctly.

Log out, go to the store.html page. Type a title of available artifacts in the search bar. Verify it works correctly.
On the same page check if all of the rest available searching (price) and sorting (category, format, seller, and sort) options work accurately.
And simultaneously verify that pagination is working correctly.

##### Selling / Bidding / Buying
	
__Selling__

Log in and click the 'Sell' icon in the` navbar`. Fill in all the input fields and do not upload any image. Click 'submit' button and verify if the item has a default picture.

Click the 'Sell' icon in the `navbar` again and try to submit the form with the Auction Price input field left blank, check if the item is in the store.

__Bidding__

Log in, go to the store page and find one of the items which you are not the seller of. On its page, click the 'Place Bid' button. And when a modal appears, check if the last bid is displayed correctly - should be the latest one or the starting one if there has not been any bid yet.

Then click one of the buttons with the set bid amount and verify the correct value appears in the Amount input. After this click the 'Bid' button and verify your bid being displayed in the Bid History section. 

Repeat the sequence for each buttons and then type your own amount less than the last bid and next the same.
Verify you received an alert message.

Then input a number higher than the last bid and check if you get an success message and the bid details appears in the Bid History table.

__Buy Now__

On the same page, click the 'Buy Now' button, you will be taken to the payment page. Fill in the form correctly and click the Submit Payment button. You should be redirect to the item page but this time both buttons are not displayed and the artifact is marked as sold. The history icon in the navbar should change its color for blue.

__Buying Items in The Cart__

When your cart is blue color instead of grey, it should contain at least one artifact that can be purchased. Click the blue button ("Buy") in the item card and check if the payment page displaying the item details (the title and the price) correctly.

Fill in the required fields for the delivery address and use one of the test numbers [Basic test card numbers](https://stripe.com/docs/testing) for the card number. Click the Submit Payment button, if all the details are correct, you should be redirect to the item page and the artifact should be marked as sold.


##### Updating / Deleting 

Log in and go to your history. Click one of "Your Sales" item which is still for sale. You should be redirected to the item page. Click "Update" button and change all the inputs in the fields including the picture. Click the Submit button. Check if the item details were updated.

On the same item page, try to leave one of the fields blank (excluding the image). Click submit button. The blank field should be indicted as required.

Go back to the item page and click "Delete" button. You should be redirected to the `item_confirm_delete` page. There click `Cancel`, you should be taken back to the item page. Click the `Delete` button again. Now you should be redirected to the store page. Check if the item is in the store no more. 

#### Bugs

The Carousel Images (home.html) are a little overstretched vertically in iPhone 5/SE. The bug did not appear in Chrome Dev Tools. I used bootstrap class *img-fluid* and then tried to limit the height of the *carousel-inner* but with no effect.

I created my own progress bar in javascript that works perfectly only in Chrome browser. Mozilla Firefox and Internet Explorer has some difficulty with interpreting this part of code *progressBar.style.width = '0px';*
```javascript
	addEventListener('load', function() {
		progressBar.style.transitionDuration = secondsStr;
		progressBar.style.width = '0px';
	});
}
```
I tried a few solution recommended on Stock Overflow. No success.

## Deployment

### Locally

You will need:
- An IDE (i.e. Eclipse, Notepad, Sublime text, Atom)
- [Python 3](https://www.python.org/downloads/)
- Install [PIP](https://pip.pypa.io/en/stable/installing/)
- Install [Git](https://www.atlassian.com/git/tutorials/install-git#:~:targetText=Install%20Git%20on%20Windows,-Git%20for%20Windows&targetText=Download%20the%20latest%20Git%20for%20Windows%20installer.,pretty%20sensible%20for%20most%20users.) 

1. Use [this](https://github.com/rafalq/Code-Institute-Project-4.git) to connect to my github account.

2. Click the button "Clone or download" and choose "Download ZIP" option. If you have git installed, you can just type the code below in your command prompt:

```
git clone https://github.com/rafalq/Code-Institute-Project-4.git
```

3. Install all required modules with the command:
 
```
pip -r requirements.txt.
```

4. Create a new database with the command:

```
python manage.py makemigrations
```
5. And propagate changes made to the database:

```
python manage.py migrate
```

7. Run the application with the command:

```
python manage.py runserver
```

8. You can visit the website at `http://127.0.0.1:8000/`


9. If you would like to login to the admin site. Run the following command:

```
python manage.py createsuperuser
```

10. Follow the instructions and then start the server again:

```
python manage.py runserver
```

11. Open a Web browser and go to “/admin/” on your local domain: `http://127.0.0.1:8000/admin/`
For more information see [Django app, part 2](https://docs.djangoproject.com/en/3.0/intro/tutorial02/)


### Heroku Deployment

1. Log into Heroku (the terminal command: `heroku login`)

2. Create a new app on the [Heroku website](https://dashboard.heroku.com/apps) by clicking the "New" button in your dashboard. Give it a name and set the region to Europe (or type in the terminal prompt: `heroku apps:create <name of your app>`)

3. Create a `requirements.txt` file using the terminal command `python -m pip freeze --local > requirements.txt`.

4. Create a `Procfile` with the terminal command `web: gunicorn <project name>.wsgi`(i.e `web: gunicorn project_name.wsgi`).

5. Create a git repository (the terminal: `git init`) 

6. Then `git add  .` , `git commit -m "Initial deployment"`, `git push` the project to GitHub.

7. Now you need to link heroku with git, using the terminal type:
`git remote add heroku <Heroku Git URL`
`git push -u heroku master`
`The URL you can get in the Settings`

8. In the heroku dashboard for the application, click on "Settings" > "Reveal Config Vars".

9. Set the following config vars:

Key  |  Value  |
--- | ---
AWS_ACCESS_KEY_ID | `<your_aws_access_key_id>`
AWS_SECRET_ACCESS_KEY | `<your_aws_secret_access_key_id>`
DATABASE_URL | `<your_database_url>`
DEBUG_VALUE | 'True'
DISABLE_COLLECTSTATIC | 1
EMAIL_PASS | `<your_email_password>`
EMAIL_USER | `<your_email_address>`
SECRET_KEY | `<django_secret_key>`
STRIPE_PUBLISHABLE | `<your_pk_test_number>`
STRIPE_SECRET | `<your_sk_test_number>`

#### IMPORTANT!

>Both __AWS_ACCESS_KEY_ID__ and __AWS_SECRET_ACCESS_KEY__, you can obtain from AWS Services. Check [AWS Identity and Access Management
](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) for more details.

>You will also need S3 [Amazon Simple Storage Service (S3)](https://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html)

>To receive __DATABASE_URL__,
1. Login to your Heroku account (see above)
2. Go to *Resources*
3. Within *Add-ons* type in "postgres" there.
4. From *Plan name* choose *Hobby Dev - Free* and click *Provision*
5. Ready. The variable should be now set in *Settings*. 

>__EMAIL_PASS__ and __EMAIL_USER__ is used for the Password Reset.

>__STRIPE_PUBLISHABLE__ and __STRIPE_SECRET__ can be obtain after registering your account with [Stripe](https://stripe.com/ie)

>To be able to use __Stripe__ for payment transaction:
>1. In the project folder go to *project_4* -> *auction_store* -> *static* -> *js* -> *payment.js*>2. Change the first line of the code using your __STRIPE_PUBLISHABLE__ number. Type it in here:

```javascript
	var stripe = Stripe('`STRIPE_PUBLISHABLE`');
```

>To be able to use the static files in Heroku:
1. Go to the location where you keep your static files (for this project `project_4`). The folder should be on the same level as the file `manage.py`.
2. Open your command prompt and use the command:

```
python manage.py collectstatic
```

>To update your database:
1. Go the directory where you keep your file `manage.py`.
2. From there type in:
```
heroku run python manage.py makemigrations
```
3. And then:
```
heroku run python manage.py migrate
```

## Credits

### Content

- The icons used in this site were obtained from [FLATICON](https://www.flaticon.com/) and [Font Awesome](https://fontawesome.com/)

- The images used in this site were obtained from [PEXELS](https://www.pexels.com/) and [Unsplash](https://unsplash.com/).

- The fonts used in this site were obtained from [Google Fonts](https://fonts.google.com/) 

- The code was corrected using Stack Overflow;  however it was significantly modified for the use of this project.

### Acknowledgements

I received inspiration for this project from [ebay](https://www.ebay.ie/). Many thanks to Corey Schafer whose youtube *Django Tutorials* videos were extremely helpful.

## Disclaimer
The content of this website is educational purposes only.
