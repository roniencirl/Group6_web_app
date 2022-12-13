from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
    send_file,
)
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from sqlite3 import Binary
from clabaireacht.database import get_database
from clabaireacht.auth import login_required


bp = Blueprint("posts", __name__)


@bp.route("/")
def index():
    db = get_database()
    posts = db.execute(
        "SELECT p.id, title, body, img, xcoord, ycoord, created, author_id, user_login, user_firstname, user_lastname"
        " FROM posts p JOIN users u ON p.author_id = u.user_id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("posts/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():

    if request.method == "GET":
        return render_template("posts/create.html")

    title = request.form["title"]
    body = request.form["body"]
    image = request.files["image"]
    xcoord = request.form["xcoord"]
    ycoord = request.form["ycoord"]
    error = None

    # TODO:  Sanitise the form input.
    print(type(image))
    print(image)
    ## Check inputs
    if "" in [title, body]:
        error = "Title is required."
    ##

    #     Binary(image)
    img_data = image.stream.read()
    print(type(img_data))
    colour = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Run in meme mode Check if integers for x-y
    if "" not in [xcoord, ycoord]:
        if not xcoord.isdigit() or not ycoord.isdigit():
            error = "Coordinates must be digits."
        else:
            xcoord = int(xcoord)
            ycoord = int(ycoord)
            # meme = cv2.imdecode(np.fromstring(img_data, dtype=np.uint8), 1)
            # cv2.putText(meme, body, (xcoord, ycoord), font, 1, colour)
            # cv2.imshow("meme", meme)
            img = Image.open(image)
            print(img.size)
            id = ImageDraw.Draw(img)
            myFont = ImageFont.truetype("FreeMono.ttf", size=40)
            id.text((xcoord, ycoord), body, font=myFont, fill=colour)
            print(type(img))
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format="jpeg")
            img_data = img_byte_arr.getvalue()

    if error is not None:
        flash(error)
    else:
        database = get_database()

        user_id = g.user["user_id"]

        if not image:
            database.execute(
                "INSERT INTO posts (title, body, author_id)" " VALUES (?, ?, ?)",
                (title, body, user_id),
            )
        else:
            database.execute(
                "INSERT INTO posts (title, body, author_id, img, xcoord, ycoord)"
                " VALUES (?, ?, ?, ?,?,?)",
                (title, body, user_id, Binary(img_data), xcoord, ycoord),
            )
        database.commit()
        return redirect(url_for("posts.index"))

    return render_template("posts/create.html")


@bp.route("/image/<int:ident>", methods=["GET"])
def image_route(ident):
    database = get_database()
    # TODO: add safety checks
    result = database.execute("select img from posts WHERE id = ?", (ident,)).fetchone()
    bytes_io = BytesIO(result[0])

    return send_file(bytes_io, mimetype="image/jpeg")
