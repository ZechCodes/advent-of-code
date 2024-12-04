const std = @import("std");

pub fn main() !void {
    var file = try std.fs.cwd().openFile("example_input.txt", .{});
    defer file.close();

    var reader = file.reader();
    var buf: [1024]u8 = undefined;

    std.debug.print("Reading file\n", .{});

    while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var iterator = std.mem.splitSequence(u8, line, "   ");
        const a = try std.fmt.parseInt(i32, iterator.next().?, 10);
        const b = try std.fmt.parseInt(i32, iterator.next().?, 10);
        std.debug.print("{d}, {d}\n", .{a, b});
    }
}
