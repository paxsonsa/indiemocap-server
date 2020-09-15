import indiemocap

def main():
    houdini_delegate = indiemocap.session_delegates.houdini.HoudiniSessionControllerDelegate()
    session_ctrl = indiemocap.session_controller.SessionController(delegate=houdini_delegate)
    indiemocap.server.start_server_with(session_ctrl)


if __name__ == "__main__":
    main()



