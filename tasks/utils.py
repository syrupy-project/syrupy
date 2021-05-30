import os


def ctx_run(ctx, *args, **kwargs):
    kwargs["pty"] = os.name == "posix"
    return ctx.run(*args, **kwargs)
