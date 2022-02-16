
====> project MASTERKLASS=====>
====>1 top business preference => one stop learning platform where users(students)
==>2 access top notch tuts on the platform.

==>**** Student ***
=> - view courses
=> enroll for course - register to enroll
=> dashboard 
        -> view course progress
        -> course workbook
        -> hours of learning
        -> mentorship with learner
=> registration

=> ****tutor ****
    =>authentication => signup and things
    => Dashboard
        => paid students of course
        => amount paid,amount made by tutor
        => tutor details

=> ***** system *****
    =>Teacher 
        =>authentication as well 
    =>Student 
        =>authentication as well
    =>Subject
        =>Modules
            =>Content
                =>video content

=> *****Models ****
    **Teacher
        => name          = character field
        => phone number  = phone no. field
        => email         = email field
        => account no.for payemnt = long integer field
        => course        => foreignKey rxnship with course
        => earned => future add for how much is earned thru the wallet
    
    **Student
        => username   => character field
        => email      => email field
        => courses_subscribed => m2m rxnship with course
        => instructor => course.instructor
        => paid_for_course => use signals to trigger this after payment is done.

    **Subject
        => course_name = characters_field
        => slug_field  => SlugField
    
    **class Course
        => instructor => foreignkey rxnship with the Tutor/teacher
        => subject => foreign key rxnship with the Subject model
        => name => model charfield()
        => slug => slugfield
        => overview => textfield overview of the course
        => created => date time field - wen the course was created.

    **Module
        => course => foreign key rxnship with the course
        => title => 
        => description => text field
        => order => how the module is to be ordered
    
    **Content
        =>module => FK with the Module itself
        => content type => will be mostly video but can aswell work with images.


    
