from tqdm import tqdm
import pandas as pd

def get_search_results(query, channel_id, youtube):
    nextPageToken = None
    items = []
    for _ in tqdm(range(20)):
        r = (
            youtube.search()
            .list(
                q=query, part="id,snippet", channelId=channel_id,
                maxResults=50, pageToken=nextPageToken
            )
            .execute()
        )
        items += r["items"]
        if "nextPageToken" not in r.keys():
            break
        nextPageToken = r["nextPageToken"]

    df = pd.DataFrame(items)
    df = pd.concat(
        [
            pd.json_normalize(df["id"]),
            pd.json_normalize(df["snippet"]),
        ],
        axis=1,
    )
    return df

def df_column_uniquify(df):
    df_columns = df.columns
    new_columns = []
    for item in df_columns:
        counter = 0
        newitem = item
        while newitem in new_columns:
            counter += 1
            newitem = "{}_{}".format(item, counter)
        new_columns.append(newitem)
    df.columns = new_columns
    return df


def get_video_stats(df, youtube):
    stats = []
    video_ids = [c for c in df["videoId"].unique() if type(c) == str]
    for i in range(0, len(video_ids), 40):
        res = (
            (youtube)
            .videos()
            .list(id=",".join(video_ids[i : i + 40]),
                  part="snippet,statistics,contentDetails,status,topicDetails,recordingDetails,localizations",
                 )
            .execute()
        )
        stats += res["items"]
    stats_df = pd.json_normalize(stats)

    df = df_column_uniquify(df)

    df_all = df.merge(
        stats_df,
        left_on=["videoId"],
        right_on=["id"],
        how="left",
        suffixes=("", "_stats"),
    )
    df_all["statistics.viewCount"] = pd.to_numeric(df_all["statistics.viewCount"])
    df_all["statistics.likeCount"] = pd.to_numeric(df_all["statistics.likeCount"])
    return df_all


KEEP_COLS = [
    "id",
    "title",
    "description",
    "publishTime",
    "kind_stats",
    "duration_seconds",
    "statistics.viewCount",
    "statistics.likeCount",
    "statistics.commentCount",
    "thumbnails.default.url",
    "thumbnails.default.width",
    "thumbnails.default.height",
    "thumbnails.medium.url",
    "thumbnails.medium.width",
    "thumbnails.medium.height",
    "thumbnails.high.url",
    "thumbnails.high.width",
    "thumbnails.high.height",
    "contentDetails.duration",
    "contentDetails.dimension",
    "topicDetails.topicCategories",
    "snippet.defaultLanguage",
    "localizations.en.title",
    "localizations.en.description",
    "snippet.tags",
]


def format_stats(df_stats):
    df_stats["publishedAt"] = pd.to_datetime(df_stats["publishedAt"])
    df_stats["publishTime"] = pd.to_datetime(df_stats["publishTime"])
    df_stats["duration"] = df_stats["contentDetails.duration"].apply(pd.Timedelta)
    df_stats["duration_seconds"] = (
        df_stats["duration"].astype("timedelta64[s]").fillna(0).astype("int")
    )

    df_final = df_stats[KEEP_COLS].copy()

    df_final = df_final.rename(
        columns={
            "statistics.viewCount": "viewCount",
            "statistics.likeCount": "likeCount",
            "statistics.favoriteCount": "favoriteCount",
            "statistics.commentCount": "commentCount",
        }
    ).copy()

    df_final["likeCount"] = pd.to_numeric(df_final["likeCount"])
    df_final["viewCount"] = pd.to_numeric(df_final["viewCount"])
    df_final["commentCount"] = pd.to_numeric(df_final["commentCount"])
    return df_final

def pull_thumbnails(df_final, channelTitle):
    if not os.path.exists(f"../out/{channelTitle}/thumbnails"):
        os.mkdir(f"../out/{channelTitle}/thumbnails")
    for i, d in df_final.dropna(subset=["thumbnails.high.url"]).iterrows():
        myurl = d["thumbnails.high.url"]
        videoId = d["id"]
        urllib.request.urlretrieve(
            myurl, f"../out/{channelTitle}/thumbnails/{videoId}.jpg"
        )

def get_channel_id(channel_name, youtube):
    res = (
        youtube.search().list(q=channel_name, part="id,snippet", maxResults=1).execute()
    )
    return res["items"][0]["snippet"]["channelId"]

def pull_all_video_info(channel_name, youtube, out_dir='./'):
    channelId = get_channel_id(channel_name, youtube)
    df = get_search_results(query="", channel_id=channelId, youtube=youtube)
    channelTitle = df["channelTitle"].values[0]
    channelTitle = "_".join(channelTitle.split(" "))
    df_stats = get_video_stats(df, youtube)
    df_final = format_stats(df_stats)

    if not os.path.exists(f"{out_dir}/{channelTitle}"):
        os.mkdir(f"{out_dir}/{channelTitle}")

    df_final.to_csv(
        f"{out_dir}/{channelTitle}/{channelTitle}_youtube_stats.csv", index=False
    )
    pull_thumbnails(df_final, channelTitle)
