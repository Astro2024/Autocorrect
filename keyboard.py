from blessed import Terminal

term = Terminal()

print("press 'esc' to quit.")
with term.cbreak():
    val = u''
    #while val not in (u'q', u'Q',):
    while format(str(val)) != "\x1b":
        val = term.inkey(timeout=20)
        if not val:
            # timeout
            print("Warning, program will auto close in a minute")
            val = term.inkey(timeout=60)

            if not val:
                val = "\x1b"

        elif val.is_sequence and val != "\x1b":
            if format(str(val)) == "\t":
                print(format(val.name))

            
            print("got sequence: {0}.".format((str(val), val.name, val.code)))
            print(format(val.name))

        elif val and val != "\x1b":
                
                print("got {0}.".format(val))
    print('bye!')